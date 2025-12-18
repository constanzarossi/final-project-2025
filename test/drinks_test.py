from app.drinks import search_ingredients, estimate_cal_per_shot

def test_search_ingredients_basic():
    ingredients = ["Vodka", "Gin", "Whiskey", "Red Vermouth"]

    assert search_ingredients(ingredients, "vod") == ["Vodka"]
    assert search_ingredients(ingredients, "GIN") == ["Gin"]
    assert search_ingredients(ingredients, "xyz") == []

def test_estimate_cal_per_shot():
    calories = estimate_cal_per_shot(40)
    assert isinstance(calories, float)
    assert 80 <= calories <= 120   
    assert estimate_cal_per_shot(None) is None


def test_estimate_cal_per_shot_zero_abv():
    assert estimate_cal_per_shot(0) == 0
