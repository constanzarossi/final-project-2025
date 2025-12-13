from flask import Blueprint, render_template, request

from app.drinks import (
    get_ingredients,
    group_ingredients_by_letter,
    search_ingredients,
    get_cocktails_by_ingredient,
    get_cocktail_details,
    get_ingredient_info,
    estimate_cal_per_shot,
)

drinks_routes = Blueprint("drinks_routes", __name__)


# ------------------------
# Page routes
# ------------------------

@drinks_routes.route("/")
def index():
    ingredients = get_ingredients()
    ingredients_by_letter = group_ingredients_by_letter(ingredients)

    return render_template(
        "index_layout.html",
        ingredients=ingredients,
        ingredients_by_letter=ingredients_by_letter,
    )


@drinks_routes.route("/ingredient/<name>")
def ingredient(name):
    cocktails = get_cocktails_by_ingredient(name)

    return render_template(
        "ingredient_layout.html",
        ingredient=name,
        cocktails=cocktails,
    )


@drinks_routes.route("/cocktail/<drink_id>")
def cocktail(drink_id):
    details = get_cocktail_details(drink_id)

    return render_template(
        "drink_layout.html",
        drink=details,
    )


# ------------------------
# API route
# ------------------------

@drinks_routes.route("/api/response.json")
def cocktails_api():
    ingredient = request.args.get("ingredient", "Vodka")

    info = get_ingredient_info(ingredient)
    abv = info["ABV"] if info else None

    return {
        "ingredient": ingredient,
        "info": info,
        "estimated_calories_per_shot": estimate_cal_per_shot(abv),
        "drinks": get_cocktails_by_ingredient(ingredient),
    }
