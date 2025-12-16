import os
from flask import Flask
from web_app.routes.drinks_routes import drinks_routes

def create_app():
    app = Flask(__name__)

    # REQUIRED for flash messages 
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

    app.register_blueprint(drinks_routes)
    return app
