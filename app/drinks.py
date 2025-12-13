import requests

BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1/"


def get_ingredients():
    """
    Fetch and return a sorted list of ingredient names.
    API call happens ONLY when this function is called.
    """
    url = BASE_URL + "list.php?i=list"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    drinks = data.get("drinks", [])
    ingredients = [
        item["strIngredient1"]
        for item in drinks
        if item.get("strIngredient1")
    ]

    return sorted(ingredients)


def group_ingredients_by_letter(ingredients):
    grouped = {}
    for ing in ingredients:
        first = ing[0].upper()
        if first.isalpha():
            grouped.setdefault(first, []).append(ing)
    return grouped


def search_ingredients(ingredients_list, term):
    term_lower = term.lower()
    return [ing for ing in ingredients_list if term_lower in ing.lower()]


def get_cocktails_by_ingredient(ingredient):
    url = BASE_URL + "filter.php?i=" + requests.utils.quote(ingredient)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("drinks", []) or []


def get_ingredient_info(ingredient):
    url = BASE_URL + "search.php?i=" + requests.utils.quote(ingredient)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    items = data.get("ingredients")
    if not items:
        return None

    info = items[0]
    abv_str = info.get("strABV")

    try:
        abv = float(abv_str) if abv_str else None
    except Exception:
        abv = None

    return {
        "Name": info.get("strIngredient"),
        "ABV": abv,
        "Description": info.get("strDescription"),
        "Type": info.get("strType"),
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
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if not data.get("drinks"):
        return None

    drink = data["drinks"][0]

    ingredients = []
    for i in range(1, 16):
        ing = drink.get(f"strIngredient{i}")
        meas = drink.get(f"strMeasure{i}")
        if ing:
            ingredients.append((ing, meas))

    return {
        "name": drink.get("strDrink"),
        "instructions": drink.get("strInstructions"),
        "ingredients": ingredients,
    }
