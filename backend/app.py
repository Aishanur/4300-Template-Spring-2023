import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import os
from dotenv import load_dotenv

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

def sql_search(ingredient): #run the code below for every ingredient to get list of recipies that have ingredient. For loop for each ingredient that we get through episode input. Then get which recipies contain all of them
    ingredient_list = [i.strip() for i in ingredient.split(',')] # split text into a list of episode titles
    query_sql = f"""SELECT * FROM recipes_reviews WHERE {' AND '.join([f"LOWER(RecipeIngredientParts) LIKE '%%{i.lower()}%%'" for i in ingredient_list])} ORDER BY AvgRecipeRating DESC LIMIT 10"""
    keys = ["ReviewId", "RecipeId", "ReviewAuthorId", "CurrentRating", "Review", "Name", "TotalTime", "DatePublished", "Description", "Image", "RecipeCategory", "Keywords", "RecipeIngredientQuantities", "RecipeIngredientParts", "ReviewCount", "Calories", "FatContent", "SaturatedFatContent", "CholesterolContent", "SodiumContent", "CarbohydrateContent", "FiberContent", "SugarContent", "ProteinContent", "RecipeInstructions", "AvgRecipeRating"]
    data = mysql_engine.query_selector(query_sql)
    return json.dumps([dict(zip(keys, i)) for i in data])

@app.route("/")
def home():
    return render_template('base.html',title="sample html")

@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)

app.run(debug=True)