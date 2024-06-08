# Pantry Pal

## Overview

Pantry Pal is an innovative application designed to help users make the most out of their available ingredients. Users can receive a ranked list of recipes they can prepare by inputting a list of ingredients and dietary restrictions. Each recipe includes a total nutritional value and breakdown, making it easy for users to make healthy choices.

## Functionality and Purpose

- **Input Ingredients**: Users can input a list of ingredients they have available, separated by commas.
- **Dietary Restrictions**: Users can specify any dietary restrictions they need to adhere to.
- **Recipe Recommendations**: The app returns a ranked list of recipes that can be made with the given ingredients.
- **Nutritional Information**: Each recipe includes detailed nutritional information.
- **User Feedback**: Users can "like" or "dislike" the recipes, and the system will update with new recommendations based on this feedback.

## Baseline Method

Our baseline method processes the input provided by the user, parses it to search through a MySQL database, and retrieves relevant recipes. The input is a list of ingredients, each separated by a comma. The method then searches the database for recipes that match these ingredients.
