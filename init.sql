CREATE DATABASE IF NOT EXISTS recipes;

USE recipes;

DROP TABLE IF EXISTS recipe_details;

CREATE TABLE recipe_details(
    id int,
    title varchar(64),
    min int,
    ingredients varchar(1024)
);

INSERT INTO recipe_details VALUES (1, 'Pineapple Ham Pizza', 60, 'olive oil, dough, tomato sauce, mozzarella cheese, ham, pineapple, red pepper flakes');
INSERT INTO recipe_details VALUES (2, 'Apple Pie', 60, 'apple, salt, milk, eggs');
INSERT INTO recipe_details VALUES (3, 'Butter Cake', 60, 'milk, yeast, unsalted butter, sugar, salt, egg, flour');
INSERT INTO recipe_details VALUES (4, 'Fattoush', 60, 'pita bread, tomatoes, red onions, pepper, cucumber, radish, scallion, lettuce, mint, sumac');
INSERT INTO recipe_details VALUES (5, 'Pizza stuffed potato', 60, 'potato, mozzarella cheese, tomato sauce, oregano leaves, garlic powder, parmesan cheese');
INSERT INTO recipe_details VALUES (6, 'Red Macaroni Salad', 60, 'Elbow Macaroni, green pepper, onion, celery, tomato, cucumber, oil, brown sugar, lemon juice, ketchup');