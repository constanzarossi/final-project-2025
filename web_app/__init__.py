from flask import Flask
from web_app.routes.drinks_routes import drinks_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(drinks_routes)
    return app
