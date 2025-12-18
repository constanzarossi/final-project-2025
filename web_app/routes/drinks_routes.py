from flask import Blueprint, render_template, request, flash

from app.drinks import (
    get_ingredients,
    group_ingredients_by_letter,
    search_ingredients,
    get_cocktails_by_ingredient,
    get_cocktail_details,
)

drinks_routes = Blueprint("drinks_routes", __name__)


# Home tab
@drinks_routes.route("/")
@drinks_routes.route("/home")
def home():
    return render_template("home_layout.html", active_page="home")


# Search tab
@drinks_routes.route("/search")
def search():
    return render_template("index_layout.html", active_page="search")


# Ingredient results
@drinks_routes.route("/ingredient")
def ingredient():
    term = request.args.get("name", "").strip()

    if not term:
        flash("Please enter an ingredient.", "warning")
        return render_template(
            "ingredient_layout.html",
            ingredient="",
            cocktails=[],
            matches=[],
            active_page="search",
        )

    ingredients = get_ingredients()
    matches = search_ingredients(ingredients, term)

    # no ingredient matches at all
    if not matches:
        flash("No ingredients found.", "warning")
        return render_template(
            "ingredient_layout.html",
            ingredient=term,
            cocktails=[],
            matches=[],
            active_page="search",
        )

    # exact match
    exact = None
    for m in matches:
        if m.lower() == term.lower():
            exact = m
            break

    if exact:
        cocktails = get_cocktails_by_ingredient(exact) or []
        if not cocktails:
            flash("No cocktails found for that ingredient.", "info")

        return render_template(
            "ingredient_layout.html",
            ingredient=exact,
            cocktails=cocktails,
            matches=[],
            active_page="search",
        )

    # partial match
    return render_template(
        "ingredient_layout.html",
        ingredient=term,
        cocktails=[],
        matches=matches[:25],
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
