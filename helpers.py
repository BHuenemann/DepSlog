from settings import *





'''
Wrapper function for recursively finding the noun phrase of a token
'''
def find_np(token):
    # finds the document, calls the recursive function, and sorts the resulting
    #  indices so that they are in order
    doc = get_doc(token)
    index_list = find_np_rec(token)
    for l in index_list:
        l.sort()

    # goes through each list of indices and substitutes the token's text into
    #  them. Then it combines the text of each noun phrase
    #
    #    EX: [[1,2,3], [6,7,8,9]] => [["the","angy","dog"], ["the","giant","rat","monster"]]
    #                             => ["the angry dog", "the giant rat monster"]
    #
    separator = ' '
    return list(map(lambda l : \
                    separator.join(list(map(lambda i : \
                                            get_text(get_token(doc, i)), l))), index_list))

'''
Recursive function for finding the noun phrase of a token.

Each noun phrase is an unsorted list of indices. Whenever this function encounters
an appositive or a conjunction, it branches into another noun phrase while keeping
track of the modifiers that have been used so far.

Returns a list of all of the noun phrase index lists associated with the token
'''
def find_np_rec(token):
    # starts with the current token's index
    index_list = [[get_index(token)]]

    # goes through the children of the token to check if they are part of the
    #  noun phrase or related to it (conjunction and appositive)
    for c in get_children(token):
        c_dep = get_dep(c)
        
        # if the dependency is that of the same noun phrase, it combines calls
        #  itself recursively and combines the results
        if c_dep in NP:
            c_np = find_np_rec(c)

            # this takes all adds the first element of index_list to all of the
            #  elements of c_np. Then it takes the result of that to replace the
            #  first element of index_list
            #
            #    EX: index_list = [[30,31,32], [40], [47]]
            #        c_np = [[35,36], [38]]
            #        =>
            #        index_list = [[30,31,32,35,36], [30,31,32,38], [40], [47]]
            #
            index_list = list(map(lambda l : index_list[0] + l, c_np)) + index_list[1:]

        # if the dependency is the prepositional word "of", it searches for a
        #  prepositional object and then adds that along with the preposition
        elif (c_dep in PREP) and (get_text(c).upper() == "OF"):
            for p in get_children(c):
                if get_dep(p) in POBJ:
                    p_np = find_np_rec(p)
                    
                    # same mapping as the example before except it includes the
                    #  index of the preposition
                    index_list = list(map(lambda l : index_list[0] + [get_index(c)] + l, p_np)) \
                        + index_list[1:]
        # if the dependency is either a conjunction or an appositive, it finds
        #  the noun phrase of that word and adds it to the end of index_list
        elif (c_dep in CONJ) or (c_dep in APPOS):
            index_list += find_np_rec(c)

    return index_list

'''
Wrapper function for recursively finding the verb phrase of a token
'''
def find_vp(token):
    # finds the document, calls the recursive function, and sorts the resulting
    #  indices so that they are in order
    doc = get_doc(token)
    index_list = find_vp_rec(token)
    index_list.sort()

    # goes through each list of indices and substitutes the token's text into
    #  them. Then it combines the text and wraps it in a list for convenience
    #  and consistency.
    #
    #    EX: [6,7,8,9] => ["the","giant","rat","monster"]
    #                  => ["the_giant_rat_monster"]
    #
    separator = '_'
    return [separator.join(list(map(lambda i : get_text(get_token(doc, i)), index_list)))]

'''
Recursive function for finding the verb phrase of a token

Returns a list of the verb phrase indices
'''
def find_vp_rec(token):
    # starts with the current token's index
    index_list = [get_index(token)]

    # iterates through the children of the token to check if they are part of the
    #  verb phrase
    for c in get_children(token):
        c_dep = get_dep(c)
        if c_dep in VP:
            index_list += find_vp_rec(c)
    
    return index_list

'''
Recursive function for finding any conjunctions for a token

Returns a list of conjunctions in token form
'''
def find_conj(token):
    # starts with the current token
    index_list = [token]

    # iterates through the children to look for any conjunctions to add to the list
    for c in get_children(token):
        if get_dep(c) in CONJ:
            index_list += find_conj(c)
            
    return index_list

'''
Alternate version of find_conj that converts the tokens into text. This version
is mainly used for printing
'''
def find_conj_text(token):
    return list(map(lambda t : get_text(t), find_conj(token)))
