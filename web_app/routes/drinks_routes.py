from flask import Blueprint, render_template, request, flash

from app.drinks import (
    get_ingredients,
    group_ingredients_by_letter,
    get_cocktails_by_ingredient,
    get_cocktail_details,
)

drinks_routes = Blueprint("drinks_routes", __name__)


# Home tab
@drinks_routes.route("/")
@drinks_routes.route("/home")
def home():
    return render_template("home_layout.html", active_page="home")


# Search tab (form page)
@drinks_routes.route("/search")
def search():
    return render_template("index_layout.html", active_page="search")


# Search results
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



# Browse tab
@drinks_routes.route("/browse")
def browse():
    ingredients = get_ingredients()
    grouped = group_ingredients_by_letter(ingredients)

    return render_template(
        "browse_layout.html",
        ingredients_by_letter=grouped,
        active_page="browse",
    )


# Cocktail detail page
@drinks_routes.route("/cocktail/<drink_id>")
def cocktail(drink_id):
    details = get_cocktail_details(drink_id)

    return render_template(
        "drink_layout.html",
        drink=details,
        active_page="search",
    )
