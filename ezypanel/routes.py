from __future__ import annotations

import re
from typing import Iterable

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .extensions import db
from .models import Domain
from .services import (
    COMMON_PHP_EXTENSIONS,
    CommandResult,
    available_extensions,
    default_php_version,
    detect_php_versions,
    detect_pool_enabled_extensions,
    disable_domain,
    domain_paths,
    delete_domain_artifacts,
    enable_domain,
    provision_domain,
    read_file,
    save_nginx_config,
    save_php_config,
    update_extensions,
)

panel_bp = Blueprint("panel", __name__)

# A stricter and fully DNS-compliant ASCII-only regex with punycode support
HOSTNAME_PATTERN = re.compile(
    r"^(xn--)?[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(\.(xn--)?[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)


def _is_valid_hostname(hostname: str) -> bool:
    if not hostname or len(hostname) > 253:
        return False
    if not HOSTNAME_PATTERN.fullmatch(hostname):
        return False

    labels = hostname.split(".")
    for label in labels:
        if not (0 < len(label) <= 63):
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
    return True


def handle_result(result: CommandResult) -> None:
    if result.success:
        flash(result.message or "Operation completed", "success")
    else:
        flash(result.message or "Operation failed", "danger")


@panel_bp.route("/")
def dashboard():
    domains = Domain.query.order_by(Domain.hostname.asc()).all()
    php_versions = detect_php_versions()
    return render_template(
        "dashboard.html",
        domains=domains,
        php_versions=php_versions,
    )


@panel_bp.route("/domains/add", methods=["POST"])
def add_domain():
    hostname = request.form.get("hostname", "").strip().lower()
    php_version = request.form.get("php_version") or default_php_version()
    notes = request.form.get("notes")
    if not hostname:
        flash("Domain is required", "danger")
        return redirect(url_for("panel.dashboard"))

    if not _is_valid_hostname(hostname):
        flash("Domain can only contain letters, numbers, hyphens, and dots.", "danger")
        return redirect(url_for("panel.dashboard"))

    if Domain.query.filter_by(hostname=hostname).first():
        flash("Domain already exists", "warning")
        return redirect(url_for("panel.dashboard"))

    paths = domain_paths(hostname, php_version)

    domain = Domain(
        hostname=hostname,
        document_root=str(paths["document_root"]),
        php_version=php_version,
        php_extensions=list(COMMON_PHP_EXTENSIONS[:3]),
        enabled=False,
        nginx_config_path=str(paths["nginx_config"]),
        php_fpm_pool_path=str(paths["php_pool"]),
        php_socket_path=str(paths["php_socket"]),
        notes=notes,
    )
    db.session.add(domain)
    db.session.commit()

    provision_domain(domain)
    flash("Domain provisioned", "success")
    return redirect(url_for("panel.dashboard"))


@panel_bp.route("/domains/<int:domain_id>")
def domain_detail(domain_id: int):
    domain = Domain.query.get_or_404(domain_id)
    nginx_config = read_file(domain.nginx_config_path)
    php_config = read_file(domain.php_fpm_pool_path)
    php_versions = detect_php_versions()
    extensions = available_extensions(domain.php_version)
    enabled_extensions = detect_pool_enabled_extensions(domain.php_socket_path)
    return render_template(
        "domain_detail.html",
        domain=domain,
        nginx_config=nginx_config,
        php_config=php_config,
        php_versions=php_versions,
        extensions=extensions,
        enabled_extensions=enabled_extensions,
    )


@panel_bp.route("/domains/<int:domain_id>/toggle", methods=["POST"])
def toggle_domain(domain_id: int):
    domain = Domain.query.get_or_404(domain_id)
    result = enable_domain(domain) if not domain.enabled else disable_domain(domain)
    handle_result(result)
    return redirect(url_for("panel.dashboard"))


@panel_bp.route("/domains/<int:domain_id>/delete", methods=["POST"])
def delete_domain(domain_id: int):
    domain = Domain.query.get_or_404(domain_id)

    if domain.enabled:
        result = disable_domain(domain)
        if not result.success:
            handle_result(result)
            return redirect(url_for("panel.dashboard"))

    cleanup_result = delete_domain_artifacts(domain)
    if not cleanup_result.success:
        handle_result(cleanup_result)
        return redirect(url_for("panel.dashboard"))

    hostname = domain.hostname
    db.session.delete(domain)
    db.session.commit()
    flash(f"Domain {hostname} deleted and all artifacts removed.", "success")
    return redirect(url_for("panel.dashboard"))


@panel_bp.route("/domains/<int:domain_id>/nginx", methods=["POST"])
def update_nginx(domain_id: int):
    domain = Domain.query.get_or_404(domain_id)
    content = request.form.get("nginx_config", "")
    result = save_nginx_config(domain, content)
    handle_result(result)
    return redirect(url_for("panel.domain_detail", domain_id=domain.id))


@panel_bp.route("/domains/<int:domain_id>/php", methods=["POST"])
def update_php(domain_id: int):
    domain = Domain.query.get_or_404(domain_id)
    content = request.form.get("php_config", "")
    php_version = request.form.get("php_version") or domain.php_version
    result = save_php_config(domain, content, php_version)
    handle_result(result)
    return redirect(url_for("panel.domain_detail", domain_id=domain.id))


# @panel_bp.route("/domains/<int:domain_id>/extensions", methods=["POST"])
# def update_extensions_route(domain_id: int):
#     domain = Domain.query.get_or_404(domain_id)
#     selected: Iterable[str] = request.form.getlist("extensions")
#     update_extensions(domain, selected)
#     flash("Extensions updated", "success")
#     return redirect(url_for("panel.domain_detail", domain_id=domain.id))
