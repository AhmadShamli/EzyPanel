from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import func

from .extensions import db


class Domain(db.Model):
    __tablename__ = "domains"

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(255), unique=True, nullable=False)
    document_root = db.Column(db.String(512), nullable=False)
    php_version = db.Column(db.String(32), nullable=False)
    php_extensions = db.Column(db.JSON, default=list)
    enabled = db.Column(db.Boolean, default=False, nullable=False)

    nginx_config_path = db.Column(db.String(512), nullable=False)
    php_fpm_pool_path = db.Column(db.String(512), nullable=False)
    php_socket_path = db.Column(db.String(512), nullable=False)

    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Domain {self.hostname} ({'enabled' if self.enabled else 'disabled'})>"

    @property
    def display_name(self) -> str:
        return self.hostname

    @property
    def system_user(self) -> str:
        """Return the system user for this domain (future proofing)."""

        return "www-data"

    @property
    def created_label(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else "-"

    @property
    def updated_label(self) -> str:
        return self.updated_at.strftime("%Y-%m-%d %H:%M") if self.updated_at else "-"
