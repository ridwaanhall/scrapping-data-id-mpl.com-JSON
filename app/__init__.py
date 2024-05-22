from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['DEBUG'] = True  # Ensure debug mode is on

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app
