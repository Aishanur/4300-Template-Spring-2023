import numpy as np

#Todo:
#funct to convert tfidf to numpy matrix
#funct to convert query (list of ingredients) into np array of length y (total num unique ingredients in dataset)
#funct to output top 10 recipes with rocchio (cos-sim)

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
