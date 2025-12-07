from flask import Blueprint, render_template, request
from app/drinks import get_ingredients_info, get_cocktails_by_ingredient, get_cocktail_details

drinks_routes = Blueprint("drinks_routes", name)


@drinks_routes.route("/")
def index():
    ingredients = get_ingredients_info()
    return render_template("index_layout.html", ingredients=ingredients)


@drinks_routes.route("/ingredient/<name>")
def ingredient(name):
    cocktails = get_cocktails_by_ingredient(name)
    return render_template("ingredient_layout.html", ingredient=name, cocktails=cocktails)


@drinks_routes.route("/cocktail/<drink_id>")
def cocktail(drink_id):
    details = get_cocktail_details(drink_id)
    return render_template("drink_layout.html", drink=details)



#api routes

@drinks_routes.route("/api/response.json")
def cocktails_api():
    print("COCKTAIL DATA (API)...")

    # for data supplied via GET request, url params are in request.args:
    url_params = dict(request.args)
    print("URL PARAMS:", url_params)

    ingredient = url_params.get("ingredient") or "Vodka"

    try:
        # Detailed info about the ingredient (ABV, type, description)
        info = get_ingredient_info(ingredient)
        abv = info["ABV"] if info else None
        est_kcal = estimate_cal_per_shot(abv)

        # List of cocktails that use this ingredient
        drinks = get_cocktails_by_ingredient(ingredient)

        return {
            "ingredient": ingredient,
            "info": info,  # can be None if API doesn't have it
            "estimated_calories_per_shot": est_kcal,
            "drinks": drinks,  # raw list from TheCocktailDB (each has idDrink, strDrink, strDrinkThumb)
        }
    except Exception as err:
        print("OOPS", err)
        return {"message": "Cocktail Data Error. Please try again."}, 404
