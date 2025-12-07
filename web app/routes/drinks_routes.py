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


#
#api routes
#

@drinks_routes.route("/api/response.json")
def cocktails_api():
    print("COCKTAIL DATA (API)...")

    url_params = dict(request.args)
    print("URL PARAMS:", url_params)

    ingredient = url_params.get("ingredient") or "Vodka"

    try:
        # ingredient info 
        info = get_ingredient_info(ingredient)
        abv = info["ABV"] if info else None
        est_kcal = estimate_cal_per_shot(abv)

        # cocktails w ingredient
        drinks = get_cocktails_by_ingredient(ingredient)

        return {
            "ingredient": ingredient,
            "info": info,  
            "estimated_calories_per_shot": est_kcal,
            "drinks": drinks,  
        }
    except Exception as err:
        print("OOPS", err)
        return {"message": "Cocktail Data Error. Please try again."}, 404
