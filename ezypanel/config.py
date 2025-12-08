from __future__ import annotations

import os
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_TEMPLATE_DIR = BASE_DIR / "config_templates"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("EZYPANEL_DATABASE_URI")
        or f"sqlite:///{(DATA_DIR / 'panel.db').as_posix()}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("EZYPANEL_SECRET_KEY", "dev-secret-key")

    DOCUMENT_ROOT_BASE = Path(
        os.environ.get("EZYPANEL_WEBROOT", DATA_DIR / "var" / "www")
    )
    NGINX_AVAILABLE_DIR = Path(
        os.environ.get(
            "EZYPANEL_NGINX_AVAILABLE", DATA_DIR / "nginx" / "sites-available"
        )
    )
    NGINX_ENABLED_DIR = Path(
        os.environ.get(
            "EZYPANEL_NGINX_ENABLED", DATA_DIR / "nginx" / "sites-enabled"
        )
    )
    PHP_FPM_BASE_DIR = Path(
        os.environ.get("EZYPANEL_PHP_FPM_BASE", DATA_DIR / "php-fpm")
    )
    PHP_SOCKET_BASE_DIR = Path(
        os.environ.get("EZYPANEL_PHP_SOCKET_BASE", DATA_DIR / "run" / "php")
    )

    NGINX_TEMPLATE_PATH = Path(
        os.environ.get(
            "EZYPANEL_NGINX_TEMPLATE",
            CONFIG_TEMPLATE_DIR / "nginx.conf.tpl",
        )
    )
    PHP_FPM_TEMPLATE_PATH = Path(
        os.environ.get(
            "EZYPANEL_PHP_FPM_TEMPLATE",
            CONFIG_TEMPLATE_DIR / "php-fpm.conf.tpl",
        )
    )

    WEB_USER = os.environ.get("EZYPANEL_WEB_USER", "www-data")
    WEB_GROUP = os.environ.get("EZYPANEL_WEB_GROUP", "www-data")

    NGINX_BIN = os.environ.get("EZYPANEL_NGINX_BIN", "nginx")
    SYSTEMCTL_BIN = os.environ.get("EZYPANEL_SYSTEMCTL_BIN", "systemctl")
    PHP_BIN_TEMPLATE = os.environ.get("EZYPANEL_PHP_BIN_TEMPLATE", "php{version}")
    PHP_FPM_SERVICE_TEMPLATE = os.environ.get(
        "EZYPANEL_PHP_FPM_SERVICE_TEMPLATE", "php{version}-fpm"
    )

    AVAILABLE_PHP_VERSIONS = os.environ.get("EZYPANEL_PHP_VERSIONS")

    SIMULATE_SERVER_COMMANDS = os.environ.get(
        "EZYPANEL_SIMULATE", "true"
    ).lower() in {"1", "true", "yes"}

    @classmethod
    def ensure_directories(cls) -> None:
        for path in [
            cls.DATA_DIR,
            cls.CONFIG_TEMPLATE_DIR,
            cls.DOCUMENT_ROOT_BASE,
            cls.NGINX_AVAILABLE_DIR,
            cls.NGINX_ENABLED_DIR,
            cls.PHP_FPM_BASE_DIR,
            cls.PHP_SOCKET_BASE_DIR,
        ]:
            Path(path).mkdir(parents=True, exist_ok=True)
