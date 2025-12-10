FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=ezypanel
ENV FLASK_ENV=production

# Add PHP repository for multiple versions
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    apt-transport-https \
    lsb-release \
    gnupg \
    wget \
    && wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg \
    && echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    unzip \
    git \
    logrotate \
    && rm -rf /var/lib/apt/lists/*

# Create persistent nginx config directories
RUN mkdir -p /app/data/nginx/sites-available \
    /app/data/nginx/sites-enabled

# Remove default nginx site dirs
RUN rm -rf /etc/nginx/sites-available /etc/nginx/sites-enabled

# Symlink nginx config dirs
RUN ln -sf /app/data/nginx/sites-available /etc/nginx/sites-available \
    && ln -sf /app/data/nginx/sites-enabled /etc/nginx/sites-enabled

# PHP 8.5 with all extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    php8.5-fpm \
    php8.5-cli \
    php8.5-common \
    php8.5-mysql \
    php8.5-pgsql \
    php8.5-sqlite3 \
    php8.5-pdo \
    php8.5-pdo-mysql \
    php8.5-pdo-pgsql \
    php8.5-pdo-sqlite \
    php8.5-xml \
    php8.5-zip \
    php8.5-mbstring \
    php8.5-curl \
    php8.5-bcmath \
    php8.5-gd \
    php8.5-intl \
    php8.5-exif \
    php8.5-soap \
    php8.5-xmlrpc \
    php8.5-imagick \
    php8.5-redis \
    php8.5-memcached \
    php8.5-ssh2 \
    php8.5-mongodb \
    php8.5-xdebug \
    && rm -rf /var/lib/apt/lists/*

# PHP 8.4 with all extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    php8.4-fpm \
    php8.4-cli \
    php8.4-common \
    php8.4-mysql \
    php8.4-pgsql \
    php8.4-sqlite3 \
    php8.4-pdo \
    php8.4-pdo-mysql \
    php8.4-pdo-pgsql \
    php8.4-pdo-sqlite \
    php8.4-xml \
    php8.4-zip \
    php8.4-mbstring \
    php8.4-curl \
    php8.4-bcmath \
    php8.4-gd \
    php8.4-intl \
    php8.4-exif \
    php8.4-soap \
    php8.4-xmlrpc \
    php8.4-imagick \
    php8.4-redis \
    php8.4-memcached \
    php8.4-ssh2 \
    php8.4-mongodb \
    php8.4-xdebug \
    && rm -rf /var/lib/apt/lists/*

# PHP 8.3 with all extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    php8.3-fpm \
    php8.3-cli \
    php8.3-common \
    php8.3-mysql \
    php8.3-pgsql \
    php8.3-sqlite3 \
    php8.3-pdo \
    php8.3-pdo-mysql \
    php8.3-pdo-pgsql \
    php8.3-pdo-sqlite \
    php8.3-xml \
    php8.3-zip \
    php8.3-mbstring \
    php8.3-curl \
    php8.3-bcmath \
    php8.3-gd \
    php8.3-intl \
    php8.3-exif \
    php8.3-soap \
    php8.3-xmlrpc \
    php8.3-imagick \
    php8.3-redis \
    php8.3-memcached \
    php8.3-ssh2 \
    php8.3-mongodb \
    php8.3-xdebug \
    && rm -rf /var/lib/apt/lists/*

# PHP 8.2 with all extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    php8.2-fpm \
    php8.2-cli \
    php8.2-common \
    php8.2-mysql \
    php8.2-pgsql \
    php8.2-sqlite3 \
    php8.2-pdo \
    php8.2-pdo-mysql \
    php8.2-pdo-pgsql \
    php8.2-pdo-sqlite \
    php8.2-xml \
    php8.2-zip \
    php8.2-mbstring \
    php8.2-curl \
    php8.2-bcmath \
    php8.2-gd \
    php8.2-intl \
    php8.2-exif \
    php8.2-soap \
    php8.2-xmlrpc \
    php8.2-imagick \
    php8.2-redis \
    php8.2-memcached \
    php8.2-ssh2 \
    php8.2-mongodb \
    php8.2-xdebug \
    && rm -rf /var/lib/apt/lists/*

# PHP 8.1 with all extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    php8.1-fpm \
    php8.1-cli \
    php8.1-common \
    php8.1-mysql \
    php8.1-pgsql \
    php8.1-sqlite3 \
    php8.1-pdo \
    php8.1-pdo-mysql \
    php8.1-pdo-pgsql \
    php8.1-pdo-sqlite \
    php8.1-xml \
    php8.1-zip \
    php8.1-mbstring \
    php8.1-curl \
    php8.1-bcmath \
    php8.1-gd \
    php8.1-intl \
    php8.1-exif \
    php8.1-soap \
    php8.1-xmlrpc \
    php8.1-imagick \
    php8.1-redis \
    php8.1-memcached \
    php8.1-ssh2 \
    php8.1-mongodb \
    php8.1-xdebug \
    && rm -rf /var/lib/apt/lists/*

# PHP 8.0 with all extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    php8.0-fpm \
    php8.0-cli \
    php8.0-common \
    php8.0-mysql \
    php8.0-pgsql \
    php8.0-sqlite3 \
    php8.0-pdo \
    php8.0-pdo-mysql \
    php8.0-pdo-pgsql \
    php8.0-pdo-sqlite \
    php8.0-xml \
    php8.0-zip \
    php8.0-mbstring \
    php8.0-curl \
    php8.0-bcmath \
    php8.0-gd \
    php8.0-intl \
    php8.0-exif \
    php8.0-soap \
    php8.0-xmlrpc \
    php8.0-imagick \
    php8.0-redis \
    php8.0-memcached \
    php8.0-ssh2 \
    php8.0-xdebug \
    && rm -rf /var/lib/apt/lists/*

# PHP 7.4 with all extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    php7.4-fpm \
    php7.4-cli \
    php7.4-common \
    php7.4-opcache \
    php7.4-mysql \
    php7.4-pgsql \
    php7.4-sqlite3 \
    php7.4-pdo \
    php7.4-pdo-mysql \
    php7.4-pdo-pgsql \
    php7.4-pdo-sqlite \
    php7.4-xml \
    php7.4-json \
    php7.4-zip \
    php7.4-mbstring \
    php7.4-curl \
    php7.4-bcmath \
    php7.4-gd \
    php7.4-intl \
    php7.4-exif \
    php7.4-soap \
    php7.4-xmlrpc \
    php7.4-imagick \
    php7.4-redis \
    php7.4-memcached \
    php7.4-ssh2 \
    php7.4-xdebug \
    && rm -rf /var/lib/apt/lists/*

# Create persistent php-fpm config roots
RUN mkdir -p /app/data/php-fpm

# Create persistent php-fpm config roots
# Create persistent php-fpm config roots with minimal resource usage www.conf tuning
RUN mkdir -p /app/data/php-fpm /app/data/run/php && \
    for v in 8.5 8.4 8.3 8.2 8.1 8.0 7.4; do \
        if [ -d /etc/php/${v}/fpm/pool.d ]; then \
            mkdir -p /app/data/php-fpm/${v}/pool.d; \
            # Copy default www.conf only if not already persisted
            if [ ! -f /app/data/php-fpm/${v}/pool.d/www.conf ]; then \
                cp /etc/php/${v}/fpm/pool.d/www.conf /app/data/php-fpm/${v}/pool.d/www.conf; \
                # Apply minimal resource usage tuning
                sed -i "s|^pm = .*|pm = static|g" /app/data/php-fpm/${v}/pool.d/www.conf; \
                sed -i "s|^pm.max_children = .*|pm.max_children = 1|g" /app/data/php-fpm/${v}/pool.d/www.conf; \
                sed -i "s|^;*pm.start_servers = .*|pm.start_servers = 1|g" /app/data/php-fpm/${v}/pool.d/www.conf; \
                sed -i "s|^;*pm.min_spare_servers = .*|pm.min_spare_servers = 1|g" /app/data/php-fpm/${v}/pool.d/www.conf; \
                sed -i "s|^;*pm.max_spare_servers = .*|pm.max_spare_servers = 1|g" /app/data/php-fpm/${v}/pool.d/www.conf; \
                sed -i "s|^;*pm.max_requests = .*|pm.max_requests = 100|g" /app/data/php-fpm/${v}/pool.d/www.conf; \
                # Lower request termination timeout for fast recycling
                sed -i "s|^;*request_terminate_timeout = .*|request_terminate_timeout = 30s|g" /app/data/php-fpm/${v}/pool.d/www.conf; \
                # Minimal logging overhead
                sed -i "s|^;*catch_workers_output = .*|catch_workers_output = yes|g" /app/data/php-fpm/${v}/pool.d/www.conf; \
                sed -i "s|^;*clear_env = .*|clear_env = no|g" /app/data/php-fpm/${v}/pool.d/www.conf; \
            fi; \
            # Replace pool.d symlink
            rm -rf /etc/php/${v}/fpm/pool.d; \
            ln -s /app/data/php-fpm/${v}/pool.d /etc/php/${v}/fpm/pool.d; \
            # Configure correct socket path
            sed -i "s|^listen = .*|listen = /app/data/run/php/php${v}-fpm.sock|g" /app/data/php-fpm/${v}/pool.d/www.conf; \
            # Create dedicated session directory for each PHP version
            mkdir -p /app/data/php/sessions/${v}; \
            chmod 1733 /app/data/php/sessions/${v}; \
            chown -R www-data:www-data /app/data/php/sessions/${v}; \
            sed -i "s|^;*session.save_path.*|session.save_path = /app/data/php/sessions/${v}|g" /etc/php/${v}/fpm/php.ini; \
        fi; \
    done


# Set default PHP version to 8.2
RUN update-alternatives --set php /usr/bin/php8.2 \
    && update-alternatives --set phar /usr/bin/phar8.2 \
    && update-alternatives --set phar.phar /usr/bin/phar.phar8.2

# Create required directories
RUN mkdir -p /var/run/php /var/log/supervisor /app/data/nginx /app/data/php-fpm /app/data/run/php /app/data/var/www /app/config_templates

RUN mkdir -p /app/data/tmp \
    /app/data/var/www/default/public \
    /app/data/var/www/default/filemanager \
    && echo "<?php phpinfo();" > /app/data/var/www/default/public/index.php \
    # Only chown document roots
    && chown -R www-data:www-data /app/data/var/www \
    # Temp directory should be world-writable with sticky bit
    && chmod 1777 /app/data/tmp

# Copy application
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download TinyFileManager
RUN mkdir -p /app/data/var/www/default/filemanager && \
    if [ ! -f "/app/data/var/www/default/filemanager/tinyfilemanager.php" ]; then \
        echo "Downloading TinyFileManager..."; \
        curl -fsSL "https://raw.githubusercontent.com/prasathmani/tinyfilemanager/refs/heads/master/tinyfilemanager.php" \
            -o "/app/data/var/www/default/filemanager/tinyfilemanager.php"; \
    fi

# Configure Nginx
RUN rm /etc/nginx/sites-enabled/default
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/ezypanel-nginx.conf /app/data/nginx/sites-available/ezypanel
RUN ln -s /app/data/nginx/sites-available/ezypanel /app/data/nginx/sites-enabled/

# Configure Supervisor
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 80 443 5000

# Copy logrotate.sh
COPY docker/logrotate.sh /app/docker/logrotate.sh
RUN chmod +x /app/docker/logrotate.sh

# Start services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
