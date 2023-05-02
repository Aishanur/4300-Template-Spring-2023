import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import random
import text


#Todo
#top10withrocchio should be changed (looks at indexes, not at recipe Ids)

def tf_idf(recipe_to_ingredients):
    """
    Parameters
    ----------
    recipe_to_ingredients: A dictionary that maps recipe ids to its ingredients

    Returns
    ----------
    np_mat: a numpy matrix, where the rows represent the recipes and the 
    columns represent the ingredients
    """
    # keys of input have type int and values have type string


    # initialize a tf-idf vectorizer
    vectorizer = TfidfVectorizer(max_df=0.8)

    # get a list of all the ingredients that appear throughout the data
    nested_ingredients = [
        # this would split all the ingredients based on the ', ' separating them, then add them into a new list
        text.remove_c_parantheses(ingredient).split(', ') 
        for ingredient in recipe_to_ingredients.values()
    ]
    # [[strawberries, milk], [bananas, milk]]

    # join the nested lists with commas to be used with fit_transform
    ingredients = [', '.join(lst) for lst in nested_ingredients]
    # ["strawberries, milk", "bananas, milk"]

    return vectorizer.fit_transform(ingredients).toarray()


def rocchio(query_vec, relevant, irrelevant, np_matrix, a=.3, b=.3, c=.8, clip = True):
    """
    Note that:
    X = total number of recipes in dataset
    Y = total number of unique ingredients in dataset

    Parameters
    ----------
    query_vec : a numpy array of size 1 x Y, such that query_vec[i] = 1 if the user has inputted the 
    ith ingredient of the dataset into the query

    relevant: list of tuples (recipeID, ingredient vector) that the user has marked relevant
    irrelevant: list of tuples (recipeID, ingredient vector) that the user has marked irrelevant

    np_matrix: matrix with X rows (representing recipes) and Y columns (representing ingredients)

    Returns:
    rocc_q: modified query vector
    """
    rocc_q = a * query_vec
    
    # when both relevant and irrelevant are empty
    if len(relevant) == 0 and len(irrelevant) == 0:
        return rocc_q
    
    # these are the 2nd and 3rd summation in the rocchio algorithm
    sum_1 = 0
    sum_2 = 0
    
    if len(relevant) != 0:
        # to sum the relevant documents' vectors
        rel_sum = np.zeros(np_matrix.shape[1])
    
        for recipeId, ing_vec in relevant:
            rel_sum += ing_vec
        
        sum_1 = b * (1/len(relevant)) * rel_sum
    
    if len(irrelevant) != 0:
        # to sum the irrelevant documents' vectors
        irrel_sum = np.zeros(np_matrix.shape[1])

        for recipeId, ing_vec in irrelevant:
            irrel_sum += ing_vec
        
        sum_2 = c * (1/len(irrelevant)) * irrel_sum
    
    rocc_q += sum_1 - sum_2
    
    if clip is True:
        indices = np.where(rocc_q >= 0, rocc_q, 0)
        return indices
    else:
        return rocc_q 

#funct to output top 10 recipes with rocchio (cos-sim)
def top10_with_rocchio(query_vec, relevant, irrelevant, np_matrix, input_rocchio, recipe_index_to_id):
    """
    Calculates cos-sim between updated query vector and all recipes containing user's initial list of ingredients
    and the updated query vector.
    Ranks the similarities and returns 10 recipes with highest score
    The results do NOT include the recipes already marked relevant
    Parameters
    ----------
    query_vec : a numpy array of size 1 x Y, such that query_vec[i] = 1 if the user has inputted the 
    ith ingredient of the dataset into the query

    recipe_no: integer i where i indicates that this query represents the ith recipe (i.e. it is some valid index of 
    the tfidf_matrix)
    
    relevant: list of pairs (recipe id, ingredient vector) where recipe_no indicates the index of the recipe marked relevant,
    and ingredient_vector is the corresponding np ingredient vector
    
    irrelevant: list of pairs (recipe id, ingredient vector) where recipe_no indicates the index of the recipe marked irrelevant,
    and ingredient_vector is the corresponding np ingredient vector    
    
    np_matrix: tfidf matrix

    input_rocchio: Rocchio algorithm implemented above

    
    Returns
    -------
    rocc_rankings (list)
        Returns a list containing the top 10 ranked recipe's ids
    """

    rocc_rankings = []

    rocc_query = input_rocchio(query_vec, relevant, irrelevant, np_matrix)
    # a dictionary of recipe ids and their corresponding cosine similarity scores
    cos_sims = {}

    #list of recipeIds of the relevant recipes
    rel_recipe_ids = [rel[0] for rel in relevant]

    #THIS IS WRONG
    # go through each recipe in the tf-idf matrix
    for j in range(len(np_matrix)):
        # the ingredient vector of the recipe we're going through
        ingredient_vec = np_matrix[j]
        
        #not a recipe marked relevant, so calculate the cos_sim
        cos_sim = np.dot(rocc_query, ingredient_vec)
        cos_sims[recipe_index_to_id[j]] = cos_sim

    #get indices of recipes with highest cos-sim scores
    sorted_recipes = sorted(cos_sims.items(), key=lambda k:k[1], reverse=True)
    
    for recipe_id, sim_score in sorted_recipes:
        if (len(rocc_rankings) >= 10):
            break

        if (recipe_id not in rel_recipe_ids):
            rocc_rankings.append(recipe_id)
        
    return rocc_rankings


def recommend_recipes(liked_recipes, disliked_recipes, tfidf_matrix, recipe_id_to_index, recipe_name_to_id, recipe_index_to_id):
    """
    Parameters
    ----------
    liked_recipes: The list containing the names of the liked recipes
    disliked_recipes: The list containing the names of the disliked recipes
        
    """
    # relevant list is the list of pairs (recipe id, recipe ingredient vector)
    # irrelevant list is the list of pairs (recipe id, recipe ingredient vector)
    relevant_lst = []
    irrelevant_lst = []

    for liked_recipe_name in liked_recipes:
        liked_recipe_id = recipe_name_to_id[liked_recipe_name]
        recipe_index = recipe_id_to_index[liked_recipe_id]
        ingredient_vector = tfidf_matrix[recipe_index]
        relevant_lst.append((liked_recipe_id, ingredient_vector))

    if (len(disliked_recipes) != 1 and disliked_recipes[0] != ''):
        for disliked_recipe_name in disliked_recipes:
            disliked_recipe_id = recipe_name_to_id[disliked_recipe_name]
            recipe_index = recipe_id_to_index[disliked_recipe_id]
            ingredient_vector = tfidf_matrix[recipe_index]
            irrelevant_lst.append((disliked_recipe_id, ingredient_vector))

    query_tpl = random.choice(relevant_lst)
  
    return top10_with_rocchio(query_tpl[1], relevant_lst, irrelevant_lst, tfidf_matrix, rocchio, recipe_index_to_id)
