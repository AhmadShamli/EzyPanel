#!/bin/bash
set -e

# PHP versions to support
PHP_VERSIONS=("8.5" "8.4" "8.3" "8.2" "8.1" "8.0" "7.4")

# Create required directories
mkdir -p /app/data/nginx/sites-available \
         /app/data/nginx/sites-enabled \
         /app/data/php-fpm \
         /app/data/run/php \
         /app/data/var/www \
         /app/data/logs/php \
         /app/data/sessions \
         /app/data/tmp

# Link Nginx site directories into /etc so new configs are picked up automatically
mkdir -p /app/data/nginx/sites-available /app/data/nginx/sites-enabled
rm -rf /etc/nginx/sites-available /etc/nginx/sites-enabled
ln -sf /app/data/nginx/sites-available /etc/nginx/sites-available
ln -sf /app/data/nginx/sites-enabled /etc/nginx/sites-enabled

# Create PHP-FPM pool directories for each version and bind them into /etc/php
for version in "${PHP_VERSIONS[@]}"; do
    DATA_POOL_DIR="/app/data/php-fpm/${version}/pool.d"
    mkdir -p "${DATA_POOL_DIR}"
    
    # Seed default PHP-FPM pool configuration if it doesn't exist
    if [ ! -f "${DATA_POOL_DIR}/www.conf" ]; then
        cp "/etc/php/${version}/fpm/pool.d/www.conf" "${DATA_POOL_DIR}/www.conf"
    fi
    
    rm -rf "/etc/php/${version}/fpm/pool.d"
    ln -sf "${DATA_POOL_DIR}" "/etc/php/${version}/fpm/pool.d"
    
    # Create PHP session directory for each version
    mkdir -p "/var/lib/php/sessions-${version}"
    
    # Set proper permissions
    chown -R www-data:www-data "/var/lib/php/sessions-${version}"
    chmod 1733 "/var/lib/php/sessions-${version}"  # Sticky bit for session directory
    
    # Configure PHP-FPM to use the correct session directory
    sed -i "s|^;session.save_path.*|session.save_path = /var/lib/php/sessions-${version}|g" "/etc/php/${version}/fpm/php.ini"
    
    # Enable PHP-FPM status page
    echo -e "\n[www-status]\nping.path = /status\nping.response = pong\n" >> "/etc/php/${version}/fpm/pool.d/www.conf"
    
    # Create PHP-FPM socket directory
    mkdir -p "/var/run/php/php${version}-fpm"
    
    # Start PHP-FPM
    service "php${version}-fpm" start
    
    echo "Configured PHP ${version} FPM"
done

# Set permissions
chown -R www-data:www-data /app/data
chmod -R 755 /app/data
chmod 1777 /app/data/tmp  # Sticky bit for tmp directory

# Create default PHP info file for testing
mkdir -p /app/data/var/www/default/public \
         /app/data/var/www/default/filemanager
echo "<?php phpinfo();" > /app/data/var/www/default/public/index.php

# Download TinyFileManager
if [ ! -f "/app/data/var/www/default/filemanager/tinyfilemanager.php" ]; then
    echo "Downloading TinyFileManager..."
    curl -fsSL "https://raw.githubusercontent.com/prasathmani/tinyfilemanager/refs/heads/master/tinyfilemanager.php" \
        -o "/app/data/var/www/default/filemanager/tinyfilemanager.php"
fi

# Initialize the database if it doesn't exist
if [ ! -f "/app/data/panel.db" ]; then
    echo "Initializing database..."
    flask db upgrade
    # Add any initial data here if needed
fi

echo "Initialization complete!"
