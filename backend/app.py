import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import os
from dotenv import load_dotenv
import math

load_dotenv()

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = os.getenv('PASSWORD')
MYSQL_PORT = 3306
MYSQL_DATABASE = "recipesdb"

mysql_engine = MySQLDatabaseHandler(MYSQL_USER,MYSQL_USER_PASSWORD,MYSQL_PORT,MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

def build_recipes():
    query_sql = f"""SELECT * FROM recipes_reviews"""
    keys = ["ReviewId", "RecipeId", "ReviewAuthorId", "CurrentRating", "Review", "Name", "TotalTime", "DatePublished", "Description", "Image", "RecipeCategory", "Keywords", "RecipeIngredientQuantities", "RecipeIngredientParts", "ReviewCount", "Calories", "FatContent", "SaturatedFatContent", "CholesterolContent", "SodiumContent", "CarbohydrateContent", "FiberContent", "SugarContent", "ProteinContent", "RecipeInstructions", "AvgRecipeRating"]
    data = mysql_engine.query_selector(query_sql)
    
    recipes = []
    seen_recipe_ids = set()

    for row in data:
        recipe_id = row[1]
        if recipe_id not in seen_recipe_ids:
            seen_recipe_ids.add(recipe_id)
            recipe = dict(zip(keys, row))
            recipes.append(recipe)
    
    return recipes

recipes_list = build_recipes()

def build_inv_idx():
    recipes = recipes_list[1:]
    
    all_ingredients = []
    for recipe in recipes:
        ingredients = ((recipe["RecipeIngredientParts"])[2:-1]).split(", ")
        all_ingredients += ingredients

    ingredients_set = set(all_ingredients)

    idx = {}
    for recipe in recipes:
        for ingredient in ingredients_set:
            if ingredient not in idx:
                if ingredient in recipe["RecipeIngredientParts"]:
                    idx[ingredient] = [recipe["RecipeId"]]
                else:
                    idx[ingredient] = []
            else:
                if ingredient in recipe["RecipeIngredientParts"]:
                    idx[ingredient].append(recipe["RecipeId"])
    return idx

inv_idx = build_inv_idx()

def compute_idf():
    idf = {}
    N = 4548
    for ingredient in inv_idx:
        id_list = inv_idx[ingredient]
        if not (len(id_list) < 3 or len(id_list)/N > 0.90):
            idf[ingredient] = math.log(N / (1 + len(id_list)), 2)
        else:
            idf[ingredient] = 0
    return idf

idf = compute_idf()
   
def sql_search(ingredient): 
    # Run the SQL query to retrieve matching recipes
    ingredient_list = [i.strip() for i in ingredient.split(', ')]
    recipe_scores = {}
    for ingredient in ingredient_list:
        for recipe_id in inv_idx[ingredient]:
            recipe_scores[recipe_id] = idf[ingredient] + recipe_scores.get(recipe_id, 0)
    sorted_scores = sorted(recipe_scores.items(), key=lambda x: x[1], reverse=True)

    results = []
    for i in range(10):
        id = sorted_scores[i][0]
        matching_recipe = next((d for d in recipes_list if d["RecipeId"] == id), None)
        ingredient_parts = matching_recipe["RecipeIngredientParts"]
        ingredients = ",".join(set(ingredient_parts[2:-1].split(",")))
        matching_recipe["RecipeIngredientParts"] = ingredients
        results.append(matching_recipe)
    return json.dumps(results)

@app.route("/")
def home():
    return render_template('base.html',title="sample html")

@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)

app.run(debug=True)