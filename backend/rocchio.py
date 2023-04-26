import numpy as np

#Todo:
#funct to convert tfidf to numpy matrix
#funct to convert query (list of ingredients) into np array of length y (total num unique ingredients in dataset)

#rocchio algorithm
def rocchio(query_vec, relevant, irrelevant, tfidf_matrix, a=.3, b=.3, c=.8, clip = True):
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

    tfidf_matrix: tfidf matrix with X rows (representing recipes) and Y columns (representing ingredients)

    Returns:
    rocc_q: modified query vector
    """

    rocc_q = a * query_vec

    agg_rel = np.zeros(len(tfidf_matrix[0]))
    agg_irrel = np.zeros(len(tfidf_matrix[0]))
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
    
    relevant: list of np ingredients vectors of the recipes that the user has liked
    
    irrelevant: list of np ingredients vectors of the recipes that the user has disliked

    tfidf_matrix: tfidf matrix with X rows (representing recipes) and Y columns (representing ingredients)

    input_rocchio: Rocchio algorithm implemented above

    Returns
    -------
    dict
        Returns the top ten highest ranked recipes for each query in the format described above.
    """
    rocc_rankings = {}

    for i in range(len(relevant)):
        rocc_query = input_rocchio(query_vec, relevant, irrelevant, tfidf_matrix)
        
        cos_sims = []
        # for j in range(len(tfidf_matrix)):
        #     if mov_ind == j:
        #         cos_sims.append(-1)
        #     elif mov_ind != j:
        #         cos_sim = np.dot(rocc_query, input_doc_matrix[j])
        #         cos_sims.append(cos_sim)
            
        
        # mov_score_lst = [(movie_index_to_name[i], s) for i,s in enumerate(cos_sims)]
        # mov_score_lst = mov_score_lst[:mov_ind] + mov_score_lst[mov_ind+1:]
        # mov_score_lst = sorted(mov_score_lst, key=lambda x: -x[1])
        
        # rocc_rankings.update({mov_name : []})
        # for name, score in mov_score_lst[:10]:
        #     rocc_rankings[mov_name].append(name)
    
    return rocc_rankings 