import math

def build_recipes(sql_engine):
    """
    Parameters
    ----------
    sql_engine: the connection to the mysql database

    Returns
    ----------
    recipes: a list of type recipes, which contains all their properties from the database
    """
    query_sql = f"""SELECT * FROM recipes_reviews"""
    keys = ["ReviewId", "RecipeId", "ReviewAuthorId", "CurrentRating", "Review", "Name", "TotalTime", "DatePublished", "Description", "Image", "RecipeCategory", "Keywords", "RecipeIngredientQuantities", "RecipeIngredientParts", "ReviewCount", "Calories", "FatContent", "SaturatedFatContent", "CholesterolContent", "SodiumContent", "CarbohydrateContent", "FiberContent", "SugarContent", "ProteinContent", "RecipeInstructions", "AvgRecipeRating"]
    data = sql_engine.query_selector(query_sql)
    
    recipes = []
    seen_recipe_ids = set()

    for row in data:
        recipe_id = row[1]
        # to avoid duplicate recipe appearances
        if recipe_id not in seen_recipe_ids:
            seen_recipe_ids.add(recipe_id)
            recipe = dict(zip(keys, row))
            recipes.append(recipe)
    
    return recipes

def get_all_ingredients(recipes_lst):
    """
    Parameters
    ----------
    recipe_lst: a list of type recipes, which contains all their properties from the database

    Returns
    ----------
    recipes: a set containing all the ingredients that appear throughout the db
    """
    recipes = recipes_lst[1:]
    
    all_ingredients = []
    for recipe in recipes:
        ingredients = ((recipe["RecipeIngredientParts"])[2:-1]).split(", ")
        all_ingredients += ingredients

    return set(all_ingredients)

def build_inv_idx(recipe_lst, ingredient_set):
    """
    Parameters
    ----------
    recipe_lst: a list of type recipes, which contains all their properties from the database
    ingredient_set: a set containing all the ingredients that appear throughout the db

    Returns
    ----------
    idx: an inverted index of the form {ingredient: [recipes the ingredient appears in]}
    """
    recipes = recipe_lst[1:]
    
    # build a dictionary {ingredient: [recipes the ingredient appears in]}
    idx = {}
    for recipe in recipes:
        for ingredient in ingredient_set:
            if ingredient not in idx:
                if ingredient in recipe["RecipeIngredientParts"]:
                    idx[ingredient] = [recipe["RecipeId"]]
                else:
                    idx[ingredient] = []
            else:
                if ingredient in recipe["RecipeIngredientParts"]:
                    idx[ingredient].append(recipe["RecipeId"])
    return idx

def compute_idf(inverted_idx):
    """
    Parameters
    ----------
    inverted_idx: an inverted index of the form {ingredient: [recipes the ingredient appears in]}

    Returns
    ----------
    idf: an dict that assigns an idf value to each ingredient
     of the form {ingredient: idf value calculated for ingredient}
    """
    idf = {}
    N = 4548
    for ingredient in inverted_idx:
        id_list = inverted_idx[ingredient]
        # Assign a non-zero idf if the ingredient appears in three documents or more and 
        # the ingredient does not appear in > 90% of all the recipes
        if not (len(id_list) < 3 or len(id_list)/N > 0.90):
            idf[ingredient] = math.log(N / (1 + len(id_list)), 2)
        else:
            idf[ingredient] = 0
    return idf