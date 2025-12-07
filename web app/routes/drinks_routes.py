from flask import Blueprint, render_template
from .cocktail_api import (
    get_ingredients,
    get_cocktails_by_ingredient,
    get_cocktail_details,
    get_ingredient_info,
    estimate_cal_per_shot
)

drinks_routes = Blueprint("drinks_routes", _name_)


@drinks_routes.route("/")
def index():
    ingredients = get_ingredients()
    return render_template("index.html", ingredients=ingredients)


@drinks_routes.route("/ingredient/<name>")
def ingredient_page(name):
    cocktails = get_cocktails_by_ingredient(name)
    info = get_ingredient_info(name)
    kcal = estimate_cal_per_shot(info["abv"]) if info else None

    return render_template(
        "ingredient.html",
        ingredient=name,
        cocktails=cocktails,
        info=info,
        kcal=kcal
    )


@drinks_routes.route("/cocktail/<drink_id>")
def cocktail_page(drink_id):
    drink = get_cocktail_details(drink_id)
    return render_template("cocktail.html", drink=drink)