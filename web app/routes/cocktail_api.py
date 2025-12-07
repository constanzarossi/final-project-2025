import request

BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1/"


def get_ingredients():
    url = BASE_URL + "list.php?i=list"
    data = requests.get(url).json()
    drinks = data.get("drinks", [])
    return sorted([d["strIngredient1"] for d in drinks])


def get_cocktails_by_ingredient(ingredient):
    url = BASE_URL + "filter.php?i=" + requests.utils.quote(ingredient)
    data = requests.get(url).json()
    return data.get("drinks", []) or []


def get_ingredient_info(ingredient):
    url = BASE_URL + "search.php?i=" + requests.utils.quote(ingredient)
    data = requests.get(url).json()
    ingredients_data = data.get("ingredients")

    if not ingredients_data:
        return None

    info = ingredients_data[0]
    abv_str = info.get("strABV")

    try:
        abv = float(abv_str) if abv_str else None
    except:
        abv = None

    return {
        "name": info.get("strIngredient"),
        "abv": abv,
        "description": info.get("strDescription"),
        "type": info.get("strType"),
    }


def estimate_cal_per_shot(abv_percent, volume_ml=44):
    if abv_percent is None:
        return None
    ethanol_density = 0.789
    alcohol_ml = volume_ml * abv_percent / 100.0
    alcohol_g = alcohol_ml * ethanol_density
    kcal = alcohol_g * 7
    return round(kcal, 2)


def get_cocktail_details(drink_id):
    url = BASE_URL + f"lookup.php?i={drink_id}"
    data = requests.get(url).json()

    if not data or not data.get("drinks"):
        return None

    d = data["drinks"][0]

    ingredients_list = []
    for i in range(1, 16):
        ing = d.get(f"strIngredient{i}")
        meas = d.get(f"strMeasure{i}")
        if ing:
            ingredients_list.append((ing, meas))

    return {
        "name": d.get("strDrink"),
        "image": d.get("strDrinkThumb"),
        "instructions": d.get("strInstructions"),
        "ingredients": ingredients_list,
    }