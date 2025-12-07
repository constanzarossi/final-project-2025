from flask import Blueprint, render_template, request
from .cocktail_api import get_ingredients, get_cocktails_by_ingredient, get_cocktail_details

drinks_routes = Blueprint("drinks_routes", _name_)


@drinks_routes.route("/")
def index():
    ingredients = get_ingredients()
    return render_template("index.html", ingredients=ingredients)


@drinks_routes.route("/ingredient/<name>")
def ingredient(name):
    cocktails = get_cocktails_by_ingredient(name)
    return render_template("ingredient.html", ingredient=name, cocktails=cocktails)


@drinks_routes.route("/cocktail/<drink_id>")
def cocktail(drink_id):
    details = get_cocktail_details(drink_id)
    return render_template("cocktail.html", drink=details)