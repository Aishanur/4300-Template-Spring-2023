# IMPLEMENT EDIT DISTANCE
# to use edit distance, what I want to do is for example,  if the user inputs oil,
# I will find the closest thing to oil, which could for example be olive oil
# The query will be the input that cannot be found in the list of ingredients
# The message will be an ingredient from the list of ingredients
# The list of messages is the list of all the ingredient names

def insertion_cost(message, j):
    return 1

def deletion_cost(query, i):
    return 1

def substitution_cost(query, message, i, j):
    return 2

def edit_matrix(query, message, ins_cost_func, del_cost_func, sub_cost_func):
    """ Calculates the edit matrix
    
    Arguments
    =========
    
    query: query string,
        
    message: message string,
    
    ins_cost_func: function that returns the cost of inserting a letter,
    
    del_cost_func: function that returns the cost of deleting a letter,
    
    sub_cost_func: function that returns the cost of substituting a letter,
    
    Returns:
        edit matrix {(i,j): int}
    """
    
    m = len(query) + 1
    n = len(message) + 1

    chart = {(0, 0): 0}
    for i in range(1, m): 
        chart[i,0] = chart[i-1, 0] + del_cost_func(query, i) 
    for j in range(1, n): 
        chart[0,j] = chart[0, j-1] + ins_cost_func(message, j)
    for i in range(1, m):
        for j in range(1, n):
            chart[i, j] = min(
                chart[i-1, j] + del_cost_func(query, i),
                chart[i, j-1] + ins_cost_func(message, j),
                chart[i-1, j-1] + sub_cost_func(query, message, i, j)
            )
    return chart

def edit_distance(query, message, ins_cost_func, del_cost_func, sub_cost_func):
    """ Finds the edit distance between a query and a message using the edit matrix
    
    Arguments
    =========
    
    query: query string,
        
    message: message string,
    
    ins_cost_func: function that returns the cost of inserting a letter,
    
    del_cost_func: function that returns the cost of deleting a letter,
    
    sub_cost_func: function that returns the cost of substituting a letter,
    
    Returns:
        edit cost (int)
    """
        
    query = query.lower()
    message = message.lower()
    
    m = len(query)
    n = len(message)
    
    edit_mat = edit_matrix(query, message, ins_cost_func, del_cost_func, sub_cost_func)
    
    return edit_mat[(m, n)]

def edit_distance_search(query, msgs):
    """ Edit distance search
    
    Arguments
    =========
    
    query: string,
        The query we are looking for.
        
    msgs: set of strings, 
    
    Returns
    =======
    
    result: the string that matches closes to the query
    """
    
    # Loop over each message, and compute the edit distance each time
    
    # initialize the best score
    best_score = {'ingredient': "", 'score': -1}

    # loop over each message
    for message in msgs:
        score = edit_distance(query, message, insertion_cost, deletion_cost, substitution_cost)
        # this is the first time the score is being calculated
        if best_score['score'] == -1:
          best_score['score'] = score
          best_score['ingredient'] = message

        # update the best score, if it is less than the previous score
        if score < best_score['score']:
          best_score['score'] = score
          best_score['ingredient'] = message
    

    return best_score['ingredient']