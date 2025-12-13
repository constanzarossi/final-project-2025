# add code here 

#UPDATED CELL
import requests
import pandas as pd
from IPython.display import display, Image

BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1/"

ingredients_url = BASE_URL + "list.php?i=list"
response = requests.get(ingredients_url)
response.raise_for_status()
data = response.json()

#Always reload JSON fresh, so data is ALWAYS a dict
data = response.json()

# Convert dict to list
data = data["drinks"]

# Extract list of ingredient names
ingredients = [item["strIngredient1"] for item in data]
ingredients = sorted(ingredients)

print("Loaded", len(ingredients), "ingredients.")


# Group ingredients by their starting letter
ingredients_by_letter = {}

for ing in ingredients:
    first = ing[0].upper()
    if first.isalpha():
        if first not in ingredients_by_letter:
            ingredients_by_letter[first] = []
        ingredients_by_letter[first].append(ing)


#Search ingredients by text match
def search_ingredients(ingredients_list, term):
    term_lower = term.lower()
    return [ing for ing in ingredients_list if term_lower in ing.lower()]


#Get cocktails that use the selected ingredient
def get_cocktails_by_ingredient(ingredient):
    url = BASE_URL + "filter.php?i=" + requests.utils.quote(ingredient)
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data.get("drinks", []) or []

    #Get detailed info about an ingredient
def get_ingredient_info(ingredient):
    url = BASE_URL + "search.php?i=" + requests.utils.quote(ingredient)
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

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
        "Name": info.get("strIngredient"),
        "ABV": abv,
        "Description": info.get("strDescription"),
        "Type": info.get("strType")
    }

#Estimate calories in a 1.5 oz (44ml) shot
def estimate_cal_per_shot(abv_percent, volume_ml=44):
    if abv_percent is None:
        return None
    ethanol_density = 0.789
    alcohol_ml = volume_ml * abv_percent / 100.0
    alcohol_g = alcohol_ml * ethanol_density
    kcal = alcohol_g * 7
    return round(kcal, 2)

#NEW 12/3

def get_cocktail_details(drink_id):
    """Fetch full ingredient list for a cocktail using its ID."""
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}"
    data = requests.get(url).json()

    if not data or not data.get("drinks"):
        return None

    drink = data["drinks"][0]

    # Extract ingredients + measures
    ingredients = []
    for i in range(1, 16):
        ing = drink.get(f"strIngredient{i}")
        meas = drink.get(f"strMeasure{i}")
        if ing:
            ingredients.append((ing, meas))

    return {
        "name": drink.get("strDrink"),
        "instructions": drink.get("strInstructions"),
        "ingredients": ingredients
    }


# Fetch info and show cocktails for the chosen ingredient
def handle_ingredient(chosen_ingredient):
    print(f"\nFetching info for ingredient: {chosen_ingredient}...")

    info = get_ingredient_info(chosen_ingredient)
    abv = info["ABV"] if info else None
    est_kcal = estimate_cal_per_shot(abv)

    print("\n--- Ingredient info ---")
    print("Name:", info["Name"] if info else chosen_ingredient)
    print("Type:", info["Type"] if info and info["Type"] else "Unknown")

    if abv is not None:
        print("ABV:", abv, "%")
    else:
        print("ABV: not available")

    if est_kcal is not None:
        print("Estimated calories per shot:", est_kcal, "kcal")

    if info and info.get("Description"):
        print("\nDescription:")
        print(info["Description"])

    print("\n------------------------")

    drinks = get_cocktails_by_ingredient(chosen_ingredient)

    if not drinks:
        print("No cocktails found.\n")
        return

    df = pd.DataFrame([
        {
            "idDrink": d.get("idDrink"),
            "Name": d.get("strDrink"),
            "Thumbnail": d.get("strDrinkThumb"),
            "Ingredient_ABV_%": abv,
            "Est_kcal_per_shot": est_kcal
        }
        for d in drinks
    ])

    print(f"\nFound {len(df)} cocktails:\n")
    display(df)

    print("\nShowing first 3 images:\n")
    for _, row in df.head(3).iterrows():
        print(row["Name"])
        if row["Thumbnail"]:
            display(Image(url=row["Thumbnail"], width=200))
        print()

    print("\n=============================================\n")

    # NEW 12/3: allow user to view full cocktail recipe
    while True:
        choice = input("Enter the index of a cocktail to see its full recipe (or 'b' to go back): ").strip()

        if choice.lower() == "b":
            print()
            return

        if not choice.isdigit() or int(choice) not in df.index:
            print("Invalid choice. Try again.\n")
            continue

        drink_id = df.loc[int(choice), "idDrink"]
        details = get_cocktail_details(drink_id)

        if not details:
            print("Could not fetch cocktail details.\n")
            continue

        print(f"\n=== {details['name']} ===\n")

        print("Ingredients:")
        for ing, meas in details["ingredients"]:
            print(f"• {ing}" + (f" — {meas}" if meas else ""))

        print("\nInstructions:")
        print(details["instructions"])

        print("\n------------------------------------------\n")

#Main menu loop for browsing/searching ingredients, finding cocktail & seeing all necessary ingredients
def main():
    print("\nUsing", len(ingredients), "ingredients.\n")

    while True:
        print("Ingredient Browser:")
        print("1. Browse ingredients by FIRST LETTER (A–Z)")
        print("2. Search ingredients by name")
        print("Type 'quit' to exit.\n")

        mode = input("Choose an option: ").strip().lower()

        if mode == "quit":
            print("Bye!")
            return

        # OPTION 1: Browse by letter
        if mode == "1":
            letter = input("Pick a letter (A–Z): ").strip().upper()

            if len(letter) != 1 or not letter.isalpha():
                print("Invalid letter.\n")
                continue

            matches = ingredients_by_letter.get(letter, [])

            if not matches:
                print(f"No ingredients starting with '{letter}'.\n")
                continue

            print(f"\nIngredients starting with '{letter}':\n")
            for idx, ing in enumerate(matches):
                print(f"{idx}: {ing}")

            choice = input("\nPick ingredient number (or 'b' to go back): ").strip()
            if choice.lower() == "b":
                print()
                continue
            if not choice.isdigit() or int(choice) >= len(matches):
                print("Invalid choice.\n")
                continue

            chosen = matches[int(choice)]
            handle_ingredient(chosen)

            again = input("Look up another ingredient? (y/n): ").strip().lower()
            if again != "y":
                print("Bye!")
                return

        # OPTION 2: Search
        elif mode == "2":
            term = input("Type part of a name (Enter = ALL): ").strip()

            if term == "":
                ing_matches = ingredients
            else:
                ing_matches = search_ingredients(ingredients, term)

            if not ing_matches:
                print("No matches.\n")
                continue

            print("\nMatching ingredients:\n")
            for idx, ing in enumerate(ing_matches):
                print(f"{idx}: {ing}")

            choice = input("\nPick ingredient number (or 'b' to go back): ").strip()
            if choice.lower() == "b":
                print()
                continue
            if not choice.isdigit() or int(choice) >= len(ing_matches):
                print("Invalid choice.\n")
                continue

            chosen = ing_matches[int(choice)]
            handle_ingredient(chosen)

            again = input("Look up another ingredient? (y/n): ").strip().lower()
            if again != "y":
                print("Bye!")
                return

        else:
            print("Invalid option.\n")

if __name__ == "__main__":
    main()





    # app/drinks.py

import requests

BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1/"

# ----------------------------
# Simple in-memory cache
# ----------------------------
_CACHE = {
    "ingredients": None,            # list[str]
    "ingredients_by_letter": None,  # dict[str, list[str]]
}


def _get_json(url: str) -> dict:
    """Helper to GET + parse JSON with basic error handling."""
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()


# ----------------------------
# Loaders (NO global API calls)
# ----------------------------
def fetch_ingredients(force_refresh: bool = False):
    """
    Fetch and return a sorted list of ingredient names.
    Cached in memory so the API is not called on import.
    """
    if (not force_refresh) and _CACHE["ingredients"] is not None:
        return _CACHE["ingredients"]

    url = BASE_URL + "list.php?i=list"
    data = _get_json(url)

    drinks = data.get("drinks") or []
    ingredients = sorted(
        [item.get("strIngredient1") for item in drinks if item.get("strIngredient1")]
    )

    _CACHE["ingredients"] = ingredients
    _CACHE["ingredients_by_letter"] = None  # invalidate dependent cache
    return ingredients


def group_ingredients_by_letter(ingredients, force_refresh: bool = False):
    """
    Group ingredients into dict: {"A": [...], "B": [...], ...}
    Cached in memory.
    """
    if (not force_refresh) and _CACHE["ingredients_by_letter"] is not None:
        return _CACHE["ingredients_by_letter"]

    by_letter = {}
    for ing in ingredients:
        if not ing:
            continue
        first = ing[0].upper()
        if first.isalpha():
            by_letter.setdefault(first, []).append(ing)

    _CACHE["ingredients_by_letter"] = by_letter
    return by_letter


# ----------------------------
# Search + API functions
# ----------------------------
def search_ingredients(ingredients_list, term):
    """Return ingredients containing term (case-insensitive)."""
    term_lower = (term or "").lower()
    return [ing for ing in ingredients_list if term_lower in ing.lower()]


def get_cocktails_by_ingredient(ingredient):
    """Return cocktails that use the given ingredient."""
    url = BASE_URL + "filter.php?i=" + requests.utils.quote(ingredient)
    data = _get_json(url)
    return data.get("drinks", []) or []


def get_ingredient_info(ingredient):
    """Return detailed info about an ingredient (ABV, type, description), or None."""
    url = BASE_URL + "search.php?i=" + requests.utils.quote(ingredient)
    data = _get_json(url)

    ingredients_data = data.get("ingredients")
    if not ingredients_data:
        return None

    info = ingredients_data[0]
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
    """Estimate calories in a shot (default 44ml) given ABV%."""
    if abv_percent is None:
        return None
    ethanol_density = 0.789  # g/ml
    alcohol_ml = volume_ml * abv_percent / 100.0
    alcohol_g = alcohol_ml * ethanol_density
    kcal = alcohol_g * 7
    return round(kcal, 2)


def get_cocktail_details(drink_id):
    """Fetch full ingredient list + instructions for a cocktail by ID."""
    url = BASE_URL + f"lookup.php?i={drink_id}"
    data = _get_json(url)

    if not data or not data.get("drinks"):
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


# ----------------------------
# Optional CLI for local testing
# (runs ONLY if you execute this file directly)
# ----------------------------
def handle_ingredient(chosen_ingredient):
    """
    CLI helper (prints to terminal).
    Keeps your original behavior but avoids any global-scope fetching.
    """
    # Lazy import so Flask/web usage doesn't need pandas/IPython
    import pandas as pd
    from IPython.display import display, Image

    print(f"\nFetching info for ingredient: {chosen_ingredient}...")

    info = get_ingredient_info(chosen_ingredient)
    abv = info["ABV"] if info else None
    est_kcal = estimate_cal_per_shot(abv)

    print("\n--- Ingredient info ---")
    print("Name:", info["Name"] if info else chosen_ingredient)
    print("Type:", info["Type"] if info and info.get("Type") else "Unknown")

    if abv is not None:
        print("ABV:", abv, "%")
    else:
        print("ABV: not available")

    if est_kcal is not None:
        print("Estimated calories per shot:", est_kcal, "kcal")

    if info and info.get("Description"):
        print("\nDescription:")
        print(info["Description"])

    print("\n------------------------")

    drinks = get_cocktails_by_ingredient(chosen_ingredient)

    if not drinks:
        print("No cocktails found.\n")
        return

    df = pd.DataFrame([
        {
            "idDrink": d.get("idDrink"),
            "Name": d.get("strDrink"),
            "Thumbnail": d.get("strDrinkThumb"),
            "Ingredient_ABV_%": abv,
            "Est_kcal_per_shot": est_kcal
        }
        for d in drinks
    ])

    print(f"\nFound {len(df)} cocktails:\n")
    display(df)

    print("\nShowing first 3 images:\n")
    for _, row in df.head(3).iterrows():
        print(row["Name"])
        if row["Thumbnail"]:
            display(Image(url=row["Thumbnail"], width=200))
        print()

    print("\n=============================================\n")

    while True:
        choice = input("Enter the index of a cocktail to see its full recipe (or 'b' to go back): ").strip()

        if choice.lower() == "b":
            print()
            return

        if not choice.isdigit() or int(choice) not in df.index:
            print("Invalid choice. Try again.\n")
            continue

        drink_id = df.loc[int(choice), "idDrink"]
        details = get_cocktail_details(drink_id)

        if not details:
            print("Could not fetch cocktail details.\n")
            continue

        print(f"\n=== {details['name']} ===\n")

        print("Ingredients:")
        for ing, meas in details["ingredients"]:
            print(f"• {ing}" + (f" — {meas}" if meas else ""))

        print("\nInstructions:")
        print(details["instructions"])
        print("\n------------------------------------------\n")


def main():
    ingredients = fetch_ingredients()
    ingredients_by_letter = group_ingredients_by_letter(ingredients)

    print("\nUsing", len(ingredients), "ingredients.\n")

    while True:
        print("Ingredient Browser:")
        print("1. Browse ingredients by FIRST LETTER (A–Z)")
        print("2. Search ingredients by name")
        print("Type 'quit' to exit.\n")

        mode = input("Choose an option: ").strip().lower()

        if mode == "quit":
            print("Bye!")
            return

        if mode == "1":
            letter = input("Pick a letter (A–Z): ").strip().upper()

            if len(letter) != 1 or not letter.isalpha():
                print("Invalid letter.\n")
                continue

            matches = ingredients_by_letter.get(letter, [])

            if not matches:
                print(f"No ingredients starting with '{letter}'.\n")
                continue

            print(f"\nIngredients starting with '{letter}':\n")
            for idx, ing in enumerate(matches):
                print(f"{idx}: {ing}")

            choice = input("\nPick ingredient number (or 'b' to go back): ").strip()
            if choice.lower() == "b":
                print()
                continue
            if not choice.isdigit() or int(choice) >= len(matches):
                print("Invalid choice.\n")
                continue

            chosen = matches[int(choice)]
            handle_ingredient(chosen)

            again = input("Look up another ingredient? (y/n): ").strip().lower()
            if again != "y":
                print("Bye!")
                return

        elif mode == "2":
            term = input("Type part of a name (Enter = ALL): ").strip()

            if term == "":
                ing_matches = ingredients
            else:
                ing_matches = search_ingredients(ingredients, term)

            if not ing_matches:
                print("No matches.\n")
                continue

            print("\nMatching ingredients:\n")
            for idx, ing in enumerate(ing_matches):
                print(f"{idx}: {ing}")

            choice = input("\nPick ingredient number (or 'b' to go back): ").strip()
            if choice.lower() == "b":
                print()
                continue
            if not choice.isdigit() or int(choice) >= len(ing_matches):
                print("Invalid choice.\n")
                continue

            chosen = ing_matches[int(choice)]
            handle_ingredient(chosen)

            again = input("Look up another ingredient? (y/n): ").strip().lower()
            if again != "y":
                print("Bye!")
                return

        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()
