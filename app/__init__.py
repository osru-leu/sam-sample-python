from flask import Flask

def create_app() -> Flask:
    """Application factory."""
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False  # keep JSON order predictable

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
