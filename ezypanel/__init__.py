from flask import Flask
from dotenv import load_dotenv
import logging

from .config import Config
from .extensions import db
from .routes import panel_bp

def create_app(config_class: type[Config] = Config) -> Flask:
    load_dotenv()
    Config.ensure_directories()

    app = Flask(__name__)
    app.config.from_object(config_class)

    level_name = app.config.get("EZYPANEL_LOG_LEVEL", "INFO")
    level = logging.getLevelName(str(level_name).upper())
    if not isinstance(level, int):
        level = logging.INFO

    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(panel_bp, url_prefix="/panel")
    return app
