from flask import Flask


def create_app() -> Flask:
    """Application factory."""
    app = Flask(__name__)

    # --- Config flags useful in tests / dev -------------------------------
    app.config["JSON_SORT_KEYS"] = False     # preserve key order in JSON
    app.config["TESTING"] = True             # flask knows we are in test mode

    # --- Register blueprints ---------------------------------------------
    from .routes import main
    app.register_blueprint(main)

    return app
