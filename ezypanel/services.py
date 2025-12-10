from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from flask import current_app

from .extensions import db
from .models import Domain


@dataclass
class CommandResult:
    success: bool
    stdout: str = ""
    stderr: str = ""

    @property
    def message(self) -> str:
        return self.stdout if self.success else self.stderr or "Command failed"


def _config_value(key: str, default=None):
    return current_app.config.get(key, default)


def _simulate() -> bool:
    return bool(_config_value("SIMULATE_SERVER_COMMANDS", True))

def _run_command(args: Sequence[str]) -> CommandResult:
    if _simulate():
        return CommandResult(True, stdout=f"Simulated: {' '.join(args)}")

    try:
        completed = subprocess.run(
            list(args),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError as exc:  # pragma: no cover - depends on system
        return CommandResult(False, stderr=str(exc))

    success = completed.returncode == 0
    return CommandResult(success, stdout=completed.stdout.strip(), stderr=completed.stderr.strip())


COMMON_PHP_EXTENSIONS = [
    "bcmath",
    "curl",
    "dom",
    "fileinfo",
    "gd",
    "imagick",
    "intl",
    "json",
    "mbstring",
    "mysqli",
    "opcache",
    "pdo_mysql",
    "redis",
    "soap",
    "xml",
    "zip",
]


def _system_php_versions() -> list[str]:
    etc_php = Path("/etc/php")
    if not etc_php.exists():
        return []

    versions: list[str] = []
    for child in etc_php.iterdir():
        if not child.is_dir():
            continue
        if any((child / subdir).exists() for subdir in ("fpm", "cli")):
            versions.append(child.name)
    return sorted(versions)


def _system_default_php_version() -> str | None:
    php_bin = shutil.which("php")
    if not php_bin:
        return None

    try:
        completed = subprocess.run(
            [php_bin, "-r", "echo PHP_MAJOR_VERSION . '.' . PHP_MINOR_VERSION;"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (OSError, ValueError):  # pragma: no cover - depends on system
        return None

    version = completed.stdout.strip()
    return version or None


def _system_php_extensions(version: str) -> list[str]:
    php_bin_template = _config_value("PHP_BIN_TEMPLATE", "php{version}")
    php_bin = php_bin_template.format(version=version)
    php_path = shutil.which(php_bin)
    if not php_path:
        return []

    try:
        completed = subprocess.run(
            [php_path, "-m"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError:  # pragma: no cover - depends on system
        return []

    modules = []
    for line in completed.stdout.splitlines():
        name = line.strip()
        if not name or name.startswith("["):
            continue
        modules.append(name.lower())

    return sorted(set(modules))

def detect_php_versions() -> list[str]:
    if not _simulate():
        system_versions = _system_php_versions()
        if system_versions:
            return system_versions

    explicit = _config_value("AVAILABLE_PHP_VERSIONS")
    if explicit:
        versions = [v.strip() for v in explicit.split(",") if v.strip()]
        if versions:
            return versions

    base_dir = Path(_config_value("PHP_FPM_BASE_DIR"))
    if base_dir.exists():
        versions = sorted({p.name for p in base_dir.iterdir() if p.is_dir()})
        if versions:
            return versions

    return ["8.2", "8.1", "7.4"]


def available_extensions(version: str | None = None) -> list[str]:
    if _simulate():
        return COMMON_PHP_EXTENSIONS

    target_version = version or _system_default_php_version()
    if not target_version:
        return COMMON_PHP_EXTENSIONS

    detected = _system_php_extensions(target_version)
    return detected or COMMON_PHP_EXTENSIONS


def default_php_version() -> str:
    if not _simulate():
        system_default = _system_default_php_version()
        if system_default:
            return system_default

    versions = detect_php_versions()
    return versions[0]


def _template_text(config_key: str, default: str) -> str:
    path = Path(_config_value(config_key))
    if path.exists():
        return path.read_text(encoding="utf-8")
    return default


def _render_template(template: str, context: dict[str, str]) -> str:
    rendered = template
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def domain_paths(hostname: str, php_version: str) -> dict[str, Path]:
    doc_root = Path(_config_value("DOCUMENT_ROOT_BASE")) / hostname / "public"
    nginx_config = Path(_config_value("NGINX_AVAILABLE_DIR")) / f"{hostname}.conf"
    php_pool = Path(_config_value("PHP_FPM_BASE_DIR")) / php_version / "pool.d" / f"{hostname}.conf"
    php_socket = Path(_config_value("PHP_SOCKET_BASE_DIR")) / f"{hostname}-{php_version}.sock"
    enabled_link = Path(_config_value("NGINX_ENABLED_DIR")) / f"{hostname}.conf"
    log_dir = Path(_config_value("DATA_DIR")) / "logs" / hostname

    return {
        "document_root": doc_root,
        "nginx_config": nginx_config,
        "php_pool": php_pool,
        "php_socket": php_socket,
        "enabled_link": enabled_link,
        "log_dir": log_dir,
    }


def _remove_path(path: Path) -> str | None:
    path = Path(path)
    try:
        if not path.exists() and not path.is_symlink():
            return None
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()
    except FileNotFoundError:
        return None
    except OSError as exc:  # pragma: no cover - depends on filesystem state
        return f"{path}: {exc}"
    return None


def ensure_domain_layout(paths: dict[str, Path]) -> None:
    paths["document_root"].mkdir(parents=True, exist_ok=True)
    paths["nginx_config"].parent.mkdir(parents=True, exist_ok=True)
    paths["php_pool"].parent.mkdir(parents=True, exist_ok=True)
    paths["enabled_link"].parent.mkdir(parents=True, exist_ok=True)
    paths["log_dir"].mkdir(parents=True, exist_ok=True)


def write_default_index(hostname: str, doc_root: Path) -> None:
    index_path = doc_root / "index.php"
    if index_path.exists():
        return
    
    template_path = Path(_config_value("CONFIG_TEMPLATE_DIR")) / "default_index.php"
    
    if template_path.exists():
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            # Replace $hostname variable in the template with the actual hostname
            index_content = template_content.replace('$hostname', hostname)
        except Exception as e:
            # Fallback to default content if template loading fails
            index_content = (
                "<?php\n"
                f"$hostname = '{hostname}';\n"
                "echo '<h1 style=\"font-family:system-ui;text-align:center;margin-top:2rem;\">'\n"
                f"     . 'Welcome to {hostname}</h1>';\n"
                "echo '<p style=\"text-align:center;color:#555;\">Error loading template. Using default content.</p>';\n"
                ">\n"
            )
    else:
        # Fallback to default content if template doesn't exist
        index_content = (
            "<?php\n"
            f"$hostname = '{hostname}';\n"
            "echo '<h1 style=\"font-family:system-ui;text-align:center;margin-top:2rem;\">'\n"
            f"     . 'Welcome to {hostname}</h1>';\n"
            "echo '<p style=\"text-align:center;color:#555;\">Template file not found. Using default content.</p>';\n"
            ">\n"
        )
    
    atomic_write(index_path, index_content)


def delete_domain_artifacts(domain: Domain) -> CommandResult:
    errors: list[str] = []

    def _remove(target: Path, label: str) -> None:
        err = _remove_path(target)
        if err:
            errors.append(f"{label} ({err})")

    base_root = Path(_config_value("DOCUMENT_ROOT_BASE")).resolve()
    document_root = Path(domain.document_root)
    domain_root = document_root.parent

    if base_root in domain_root.parents:
        _remove(domain_root, "document root")
    else:
        _remove(document_root, "document root")

    _remove(Path(domain.nginx_config_path), "nginx config")
    _remove(Path(domain.php_fpm_pool_path), "php-fpm pool config")
    _remove(Path(domain.php_socket_path), "php socket")

    paths = domain_paths(domain.hostname, domain.php_version)
    _remove(paths["enabled_link"], "nginx enabled symlink")
    _remove(paths["log_dir"], "log directory")

    if errors:
        return CommandResult(False, stderr="; ".join(errors))
    return CommandResult(True, stdout=f"Removed files for {domain.hostname}")


def _logs_for_domain(domain: Domain) -> tuple[Path, Path]:
    log_dir = Path(_config_value("DATA_DIR")) / "logs" / domain.hostname
    access = log_dir / "access.log"
    error = log_dir / "error.log"
    log_dir.mkdir(parents=True, exist_ok=True)
    return access, error


def nginx_template(domain: Domain) -> str:
    access_log, error_log = _logs_for_domain(domain)
    default_template = (
        "server {\n"
        "    listen 80;\n"
        "    server_name {{HOSTNAME}};\n"
        "    root {{DOCUMENT_ROOT}};\n"
        "    index index.php index.html;\n"
        "\n"
        "    access_log {{ACCESS_LOG}};\n"
        "    error_log {{ERROR_LOG}};\n"
        "\n"
        "    location / {\n"
        "        try_files $uri $uri/ /index.php?$query_string;\n"
        "    }\n"
        "\n"
        "    location ~ \\.php$ {\n"
        "        include fastcgi_params;\n"
        "        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;\n"
        "        fastcgi_pass unix:{{PHP_SOCKET}};\n"
        "    }\n"
        "}\n"
    )
    template = _template_text("NGINX_TEMPLATE_PATH", default_template)
    context = {
        "HOSTNAME": domain.hostname,
        "DOCUMENT_ROOT": domain.document_root,
        "PHP_SOCKET": domain.php_socket_path,
        "ACCESS_LOG": str(access_log),
        "ERROR_LOG": str(error_log),
    }
    return _render_template(template, context).strip()


def php_fpm_template(domain: Domain) -> str:
    user = _config_value("WEB_USER")
    group = _config_value("WEB_GROUP")
    default_template = (
        "[{{HOSTNAME}}]\n"
        "user = {{WEB_USER}}\n"
        "group = {{WEB_GROUP}}\n"
        "listen = {{PHP_SOCKET}}\n"
        "listen.owner = {{WEB_USER}}\n"
        "listen.group = {{WEB_GROUP}}\n"
        "listen.mode = 0660\n"
        "pm = dynamic\n"
        "pm.max_children = 5\n"
        "pm.start_servers = 2\n"
        "pm.min_spare_servers = 1\n"
        "pm.max_spare_servers = 3\n"
        "php_admin_value[memory_limit] = 256M\n"
        "php_admin_value[upload_max_filesize] = 50M\n"
    )
    template = _template_text("PHP_FPM_TEMPLATE_PATH", default_template)
    context = {
        "HOSTNAME": domain.hostname,
        "PHP_SOCKET": domain.php_socket_path,
        "WEB_USER": user,
        "WEB_GROUP": group,
    }
    return _render_template(template, context).strip()


def atomic_write(path: Path, content: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    backup_path = path.with_suffix(path.suffix + ".bak")

    if path.exists():
        shutil.copy2(path, backup_path)

    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    tmp_path.write_text(normalized, encoding="utf-8")
    tmp_path.replace(path)


def read_file(path: str | Path) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8")


def test_nginx() -> CommandResult:
    nginx_bin = _config_value("NGINX_BIN")
    return _run_command([nginx_bin, "-t"])


def reload_nginx() -> CommandResult:
    nginx_bin = _config_value("NGINX_BIN")
    return _run_command([nginx_bin, "-s", "reload"])


def reload_php_fpm(version: str) -> CommandResult:
    tmpl = _config_value("PHP_FPM_SERVICE_TEMPLATE")
    service_name = tmpl.format(version=version)
    systemctl = _config_value("SYSTEMCTL_BIN")
    return _run_command([systemctl, "reload", service_name])


def _create_symlink(source: Path, link: Path) -> None:
    if link.exists() or link.is_symlink():
        link.unlink()
    try:
        link.symlink_to(source)
    except (OSError, NotImplementedError):  # pragma: no cover - depends on OS
        shutil.copy2(source, link)


def enable_domain(domain: Domain) -> CommandResult:
    paths = domain_paths(domain.hostname, domain.php_version)
    available = paths["nginx_config"]
    enabled = paths["enabled_link"]
    if not available.exists():
        return CommandResult(False, stderr="Nginx config missing; provision domain first.")

    _create_symlink(available, enabled)

    test_result = test_nginx()
    if not test_result.success:
        if enabled.exists():
            enabled.unlink()
        return CommandResult(False, stderr=f"nginx -t failed: {test_result.stderr}")

    reload_result = reload_nginx()
    if reload_result.success:
        domain.enabled = True
        db.session.commit()
        return reload_result

    # rollback
    if enabled.exists():
        enabled.unlink()
    return CommandResult(False, stderr=f"Reload failed: {reload_result.stderr}")


def disable_domain(domain: Domain) -> CommandResult:
    paths = domain_paths(domain.hostname, domain.php_version)
    enabled = paths["enabled_link"]
    if enabled.exists() or enabled.is_symlink():
        enabled.unlink()

    test_result = test_nginx()
    if not test_result.success:
        return CommandResult(False, stderr=f"nginx -t failed: {test_result.stderr}")

    reload_result = reload_nginx()
    if reload_result.success:
        domain.enabled = False
        db.session.commit()
        return reload_result

    return CommandResult(False, stderr=f"Reload failed: {reload_result.stderr}")


def provision_domain(domain: Domain) -> None:
    paths = domain_paths(domain.hostname, domain.php_version)
    ensure_domain_layout(paths)

    domain.document_root = str(paths["document_root"])
    domain.nginx_config_path = str(paths["nginx_config"])
    domain.php_fpm_pool_path = str(paths["php_pool"])
    domain.php_socket_path = str(paths["php_socket"])

    db.session.commit()

    write_default_index(domain.hostname, paths["document_root"])
    atomic_write(paths["nginx_config"], nginx_template(domain))
    atomic_write(paths["php_pool"], php_fpm_template(domain))

    enable_domain(domain)


def save_nginx_config(domain: Domain, content: str) -> CommandResult:
    atomic_write(Path(domain.nginx_config_path), content)
    test_result = test_nginx()
    if not test_result.success:
        return CommandResult(False, stderr=f"nginx -t failed: {test_result.stderr}")
    return reload_nginx()


def save_php_config(domain: Domain, content: str, php_version: str) -> CommandResult:
    original_version = domain.php_version
    original_socket = domain.php_socket_path

    if php_version != domain.php_version:
        paths = domain_paths(domain.hostname, php_version)
        domain.php_version = php_version
        domain.php_fpm_pool_path = str(paths["php_pool"])
        domain.php_socket_path = str(paths["php_socket"])
        domain.nginx_config_path = domain.nginx_config_path  # unchanged path
    else:
        paths = {
            "php_pool": Path(domain.php_fpm_pool_path),
            "php_socket": Path(domain.php_socket_path),
        }

    atomic_write(Path(domain.php_fpm_pool_path), content)

    if php_version != original_version:
        # Update nginx config socket reference
        nginx_path = Path(domain.nginx_config_path)
        nginx_content = read_file(nginx_path)
        nginx_content = nginx_content.replace(original_socket, domain.php_socket_path)
        atomic_write(nginx_path, nginx_content)

    db.session.commit()

    nginx_test = test_nginx()
    if not nginx_test.success:
        return CommandResult(False, stderr=f"nginx -t failed: {nginx_test.stderr}")

    reload_nginx()
    reload_result = reload_php_fpm(domain.php_version)
    if not reload_result.success:
        return CommandResult(False, stderr=f"PHP-FPM reload failed: {reload_result.stderr}")

    return CommandResult(True, stdout="PHP-FPM pool updated")


def update_extensions(domain: Domain, extensions: Iterable[str]) -> None:
    domain.php_extensions = sorted(set(extensions))
    db.session.commit()


def domain_summary(domain: Domain) -> dict[str, str]:
    return {
        "hostname": domain.hostname,
        "document_root": domain.document_root,
        "nginx_config": domain.nginx_config_path,
        "php_pool": domain.php_fpm_pool_path,
        "php_socket": domain.php_socket_path,
    }
