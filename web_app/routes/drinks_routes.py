from flask import Blueprint, render_template, request

from app.drinks import (
    get_ingredients,
    search_ingredients,
    get_cocktails_by_ingredient,
    get_cocktail_details,
)

drinks_routes = Blueprint("drinks_routes", __name__)


# Home (instructions)
@drinks_routes.route("/")
@drinks_routes.route("/home")
def home():
    return render_template("home_layout.html", active_page="home")


# Search page (form)
@drinks_routes.route("/search")
def search_page():
    return render_template("index_layout.html", active_page="search")


# Ingredient results + suggestions
@drinks_routes.route("/ingredient")
def ingredient():
    term = request.args.get("name", "").strip()

    # If empty, just show the page with a message
    if not term:
        return render_template(
            "ingredient_layout.html",
            ingredient="",
            cocktails=[],
            matches=[],
            active_page="search",
        )

    # Find matches from full ingredient list
    ingredients = get_ingredients()
    matches = search_ingredients(ingredients, term)

    # Check for exact match (case-insensitive)
    exact = None
    for m in matches:
        if m.lower() == term.lower():
            exact = m
            break

    # If exact match, fetch cocktails
    if exact:
        cocktails = get_cocktails_by_ingredient(exact)
        return render_template(
            "ingredient_layout.html",
            ingredient=exact,
            cocktails=cocktails,
            matches=[],
            active_page="search",
        )

    # Otherwise show suggestions (partial input)
    return render_template(
        "ingredient_layout.html",
        ingredient=term,
        cocktails=[],
        matches=matches[:25],
        active_page="search",
    )


# Cocktail detail page
@drinks_routes.route("/cocktail/<drink_id>")
def cocktail(drink_id):
    drink = get_cocktail_details(drink_id)
    return render_template(
        "drink_layout.html",
        drink=drink,
        active_page="search",
    )
