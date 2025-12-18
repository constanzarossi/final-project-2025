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
        "image": drink.get("strDrinkThumb"),
    }


# TERMINAL APP

def print_ingredient_info(ingredient):
    info = get_ingredient_info(ingredient)
    if not info:
        print("\nIngredient info not found.\n")
        return

    abv = info.get("ABV")
    kcal = estimate_cal_per_shot(abv) if abv is not None else None

    print("\n--- Ingredient Info ---")
    print("Name:", info.get("Name"))
    print("Type:", info.get("Type") or "Unknown")
    print("ABV:", f"{abv}%" if abv is not None else "N/A")
    print("Estimated kcal per 1.5oz:", kcal if kcal is not None else "N/A")
    if info.get("Description"):
        print("\nDescription:")
        print(info["Description"])
    print("------------------------\n")


def main():
    print("\nCocktail Explorer (Terminal Mode)")
    print("--------------------------------\n")

    # Load ingredient list
    try:
        ingredients = get_ingredients()
    except Exception as e:
        print("Error loading ingredients:", e)
        return

    print(f"Loaded {len(ingredients)} ingredients.\n")

    while True:
        term = input("Type an ingredient (full or partial), or 'quit': ").strip()
        if term.lower() == "quit":
            print("Bye!")
            return
        if not term:
            print("Please type something.\n")
            continue

        matches = search_ingredients(ingredients, term)

        if not matches:
            print("No ingredients found.\n")
            continue

        # If not exact, show suggestions to pick from
        exact = None
        for m in matches:
            if m.lower() == term.lower():
                exact = m
                break

        if not exact:
            print("\nDid you mean:")
            for i, m in enumerate(matches[:20]):
                print(f"{i}: {m}")

            choice = input("\nPick a number (or 'b' to go back): ").strip().lower()
            if choice == "b":
                print()
                continue
            if not choice.isdigit() or int(choice) not in range(0, min(20, len(matches))):
                print("Invalid choice.\n")
                continue

            exact = matches[int(choice)]

        print_ingredient_info(exact)

        try:
            drinks = get_cocktails_by_ingredient(exact)
        except Exception as e:
            print("Error fetching cocktails:", e)
            continue

        if not drinks:
            print("No cocktails found for that ingredient.\n")
            continue

        print(f"Found {len(drinks)} cocktails using {exact}:\n")
        for i, d in enumerate(drinks[:25]):
            print(f"{i}: {d.get('strDrink')} (id={d.get('idDrink')})")

        while True:
            choice = input("\nEnter cocktail number for recipe (or 'b' back): ").strip().lower()
            if choice == "b":
                print()
                break
            if not choice.isdigit() or int(choice) not in range(0, min(25, len(drinks))):
                print("Invalid choice.\n")
                continue

            drink_id = drinks[int(choice)].get("idDrink")
            details = get_cocktail_details(drink_id)
            if not details:
                print("Could not fetch details.\n")
                continue

            print(f"\n=== {details['name']} ===")
            print("\nIngredients:")
            for ing, meas in details["ingredients"]:
                print(f"• {ing}" + (f" — {meas}" if meas else ""))
            print("\nInstructions:")
            print(details["instructions"])
            print("\n------------------------\n")


if __name__ == "__main__":
    main()