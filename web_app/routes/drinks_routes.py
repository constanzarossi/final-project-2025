from flask import Blueprint, render_template, request

from app.drinks import (
    get_ingredients,
    group_ingredients_by_letter,
    get_cocktails_by_ingredient,
    get_cocktail_details,
)

drinks_routes = Blueprint("drinks_routes", __name__)


# ------------------------
# Tab 1: Search
# ------------------------
@drinks_routes.route("/")
def index():
    return render_template("index_layout.html", active_page="search")


# ------------------------
# Search results
# ------------------------
@drinks_routes.route("/ingredient")
def ingredient():
    name = request.args.get("name", "").strip()
    cocktails = get_cocktails_by_ingredient(name) if name else []

    return render_template(
        "ingredient_layout.html",
        ingredient=name,
        cocktails=cocktails,
        active_page="search",
    )


# ------------------------
# Tab 2: Browse ingredients
# ------------------------
@drinks_routes.route("/browse")
def browse():
    ingredients = get_ingredients()
    grouped = group_ingredients_by_letter(ingredients)

    return render_template(
        "browse_layout.html",
        ingredients_by_letter=grouped,
        active_page="browse",
    )


# ------------------------
# Cocktail detail
# ------------------------
@drinks_routes.route("/cocktail/<drink_id>")
def cocktail(drink_id):
    details = get_cocktail_details(drink_id)

    return render_template(
        "drink_layout.html",
        drink=details,
        active_page="search",
    )

