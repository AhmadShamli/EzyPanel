# EzyPanel - Simple Web Hosting Control Panel

EzyPanel is a lightweight and easy-to-use web hosting control panel for managing websites, domains, and server configurations. Built with Python and Flask, it provides a clean interface for managing Nginx, PHP-FPM, and more.

![EzyPanel Screenshot](https://via.placeholder.com/800x500.png?text=EzyPanel+Dashboard+Screenshot)

## Features

- 🚀 Simple domain management with one-click setup
- 🌐 Nginx configuration management
- 🐘 Multi-PHP version support (7.4, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5)
- 🐳 Docker support for easy deployment
- 🔄 Easy enable/disable domains
- 🗑️ Complete domain removal with cleanup
- 📝 Default index page template for new domains
- 🛠️ Built-in configuration validation
- 🔒 Secure defaults with PHP-FPM isolation

## Prerequisites

### For Manual Installation
- Python 3.8+
- Nginx
- PHP-FPM (multiple versions supported)
- SQLite (or other SQLAlchemy-supported database)
- System packages: `nginx`, `php-fpm`, `python3-venv`

### For Docker Installation
- Docker 20.10.0+
- Docker Compose 2.0.0+

## Installation

### Option 1: Docker Installation (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/AhmadShamli/EzyPanel.git
   cd EzyPanel
   ```

2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   (Optional) Edit the `.env` file to customize settings.

3. Start the services:
   ```bash
   docker-compose up -d --build
   ```

4. The application will be available at `http://localhost:5000`

### Option 2: Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AhmadShamli/EzyPanel.git
   cd EzyPanel
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix or MacOS:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the application:
   - Copy `.env.example` to `.env` and update the configuration as needed
   - Set up the required directories and permissions

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```ini
FLASK_APP=ezypanel
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///data/panel.db

# Web server settings
WEB_USER=www-data
WEB_GROUP=www-data

# Path settings
DOCUMENT_ROOT_BASE=./data/var/www
NGINX_AVAILABLE_DIR=./data/nginx/sites-available
NGINX_ENABLED_DIR=./data/nginx/sites-enabled
PHP_FPM_BASE_DIR=./data/php-fpm
PHP_SOCKET_BASE_DIR=./data/run/php

# Binary paths (update these according to your system)
NGINX_BIN=nginx
SYSTEMCTL_BIN=systemctl

# Set to False in production
SIMULATE_SERVER_COMMANDS=True
```

## Running the Application

### Docker (Recommended)
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Installation

#### Development
```bash
flask run --host=0.0.0.0 --port=5000
```

#### Production
For production, use a WSGI server like Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "ezypanel:create_app()"
```

## Usage

1. Access the web interface at `http://localhost:5000`
2. Add your first domain through the dashboard
3. Configure Nginx and PHP-FPM settings as needed
4. Upload your website files to the domain's document root

## Default Index Page

New domains will automatically get a default index page with server information. You can customize this by modifying the template at `config_templates/default_index.php`.

## Project Structure

```
EzyPanel/
├── docker/               # Docker configuration files
│   ├── nginx.conf       # Nginx main configuration
│   ├── ezypanel-nginx.conf  # EzyPanel Nginx site config
│   ├── supervisord.conf # Process management
│   └── init.sh          # Initialization script
├── config_templates/    # Configuration templates
│   └── default_index.php  # Default website index template
├── data/                # Application data (mounted volume in Docker)
│   ├── logs/            # Domain access/error logs
│   ├── nginx/           # Nginx configurations
│   ├── php-fpm/         # PHP-FPM configurations
│   └── var/www/         # Website document roots
├── ezypanel/           # Application package
│   ├── static/         # Static files (CSS, JS, images)
│   ├── templates/      # HTML templates
│   ├── __init__.py     # Application factory
│   ├── config.py       # Configuration settings
│   ├── extensions.py   # Flask extensions
│   ├── models.py       # Database models
│   ├── routes.py       # Application routes
│   └── services.py     # Business logic
├── .env.example       # Example environment variables
├── .gitignore         # Git ignore file
├── app.py             # Application entry point
├── config.py          # Configuration (deprecated, use .env)
└── requirements.txt   # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## PHP Version Management

EzyPanel supports multiple PHP versions (7.4, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5) with the following extensions pre-installed for each version:

- Core: cli, fpm, common, opcache
- Database: mysql, pgsql, sqlite3, pdo, pdo-mysql, pdo-pgsql, pdo-sqlite
- Extensions: xml, json, zip, mbstring, curl, bcmath, gd, intl, exif, soap, sodium, xmlrpc, imagick
- Caching: redis, memcached
- Other: ssh2, mongodb, xdebug

### Switching PHP Versions

When adding a new domain, you can select the desired PHP version from the web interface. Each domain can use a different PHP version.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Inspired by various open-source control panels
- Icons from [Font Awesome](https://fontawesome.com/)

---

**Note:** EzyPanel is currently in development. Use in production at your own risk.
