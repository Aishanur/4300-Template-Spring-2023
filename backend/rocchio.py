import numpy as np

#Todo:
#funct to convert tfidf to numpy matrix
#funct to convert query (list of ingredients) into np array of length y (total num unique ingredients in dataset)

def inv_index_to_np(index, ingredient_set):
    """
    Parameters
    ----------
    index: a dictionary, of the form {ingredients: [recipes the ingredient appears in]}

    ingredient_set: a set containing all ingredients present throughout the database

    Returns:
    np_mat: a numpy matrix, where the rows represent the recipes and the 
    columns represent the ingredients
    """
    pass


#rocchio algorithm
def rocchio(query_vec, relevant, irrelevant, np_matrix, a=.3, b=.3, c=.8, clip = True):
    """
    Note that:
    X = total number of recipes in dataset
    Y = total number of unique ingredients in dataset

    Parameters
    ----------
    query_vec : a numpy array of size 1 x Y, such that query_vec[i] = 1 if the user has inputted the 
    ith ingredient of the dataset into the query

    relevant: list of np ingredients vectors of the recipes that the user has liked
    irrelevant: list of np ingredients vectors of the recipes that the user has disliked

    np_matrix: matrix with X rows (representing recipes) and Y columns (representing ingredients)

    Returns:
    rocc_q: modified query vector
    """

    rocc_q = a * query_vec

    agg_rel = np.zeros(len(np_matrix[0]))
    agg_irrel = np.zeros(len(np_matrix[0]))
    len_rel = len(relevant)
    len_irrel = len(irrelevant)

    for i in range(len_rel):
        agg_rel += relevant[i]
    
    if len_rel != 0:
        agg_rel /= len_rel
     
    for i in range(len_irrel):
        agg_irrel += irrelevant[i]
    
    if len_irrel != 0:
        agg_irrel /= len_irrel
    
    rocc_q += ((b * agg_rel) - (c * agg_irrel))
    
    if clip:
        rocc_q[rocc_q < 0] = 0
    
    rocc_q += 0.

    return rocc_q

#funct to output top 10 recipes with rocchio (cos-sim)
def top10_with_rocchio(query_vec, relevant, irrelevant, tfidf_matrix, input_rocchio):
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
    
    relevant: list of pairs (recipe_no, ingredient vector) where recipe_no indicates the index of the recipe marked relevant,
    and ingredient_vector is the corresponding np ingredient vector
    
    irrelevant: list of pairs (recipe_no, ingredient vector) where recipe_no indicates the index of the recipe marked irrelevant,
    and ingredient_vector is the corresponding np ingredient vector    
    
    tfidf_matrix: tfidf matrix with X rows (representing recipes) and Y columns (representing ingredients)
    
    input_rocchio: Rocchio algorithm implemented above
    
    Returns
    -------
    rocc_rankings (dict)
        Returns dict of 10 (recipe_no, ingredient vector) pairs which have highest cosine similarity with modified 
        query vector and are NOT the recipes already marked relevant
        
    """
    rocc_rankings = {}

    rocc_query = input_rocchio(query_vec, relevant, irrelevant, tfidf_matrix)
    cos_sims = []

    rel_recipe_nos = [rel[0] for rel in relevant]

    for j in range(len(tfidf_matrix)):
        #if this is a recipe already marked relevant, we don't want to return it in our new results
        if j in rel_recipe_nos:
            cos_sim.append(-1)
        
        #not a recipe marked relevant, so calculate the cos_sim
        else:
            cos_sim = np.dot(rocc_query, tfidf_matrix[j])
            cos_sims.append(cos_sim)

    #get indices of recipes with highest cos-sim scores
    top10_recipe_nos = sorted(range(len(cos_sims)), key=lambda i: cos_sims[i], reverse=True)[:10]

    for i in range(10):
        #grab index of one of the top ten ranked recipes
        recipe_no = top10_recipe_nos[i]
        rocc_rankings.update({ recipe_no: tfidf_matrix[recipe_no]})

    return rocc_rankings
