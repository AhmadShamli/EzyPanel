from flask import Flask
from .config import Config
from .extensions import db
from .routes import panel_bp

def create_app(config_class: type[Config] = Config) -> Flask:
    Config.ensure_directories()

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(panel_bp)
    return app
