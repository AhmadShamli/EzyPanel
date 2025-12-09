#!/bin/bash
set -euo pipefail

NGINX_BIN=${NGINX_BIN:-/usr/sbin/nginx}
SYSTEMCTL_BIN=${SYSTEMCTL_BIN:-/bin/systemctl}
STATE_FILE="/tmp/ezypanel-logrotate.status"
CONF_FILE="/tmp/ezypanel-logrotate.conf"

cat >"${CONF_FILE}" <<'EOF'
/var/log/nginx/*.log /var/log/php*-fpm.log /app/data/logs/*.log /app/data/logs/php/*.log {
    daily
    rotate 7
    missingok
    notifempty
    compress
    delaycompress
    create 0640 www-data www-data
    sharedscripts
    copytruncate
    postrotate
        if [ -x "${NGINX_BIN}" ]; then
            "${NGINX_BIN}" -t >/dev/null 2>&1 && "${SYSTEMCTL_BIN}" reload nginx >/dev/null 2>&1 || true
        fi
    endscript
}
EOF

logrotate -s "${STATE_FILE}" "${CONF_FILE}"
