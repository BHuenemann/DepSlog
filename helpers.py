from settings import *





'''
Wrapper function for recursively finding the noun phrase of a token
'''
def find_np(token, conj = True):
    # finds the document, calls the recursive function, and sorts the resulting
    #  indices so that they are in order
    doc = get_doc(token)
    index_list = find_np_rec(token, conj)
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
def find_np_rec(token, conj):
    # starts with the current token's index
    index_list = [[get_index(token)]]

    # goes through the children of the token to check if they are part of the
    #  noun phrase or related to it (conjunction and appositive)
    for c in get_children(token):
        c_dep = get_dep(c)
        
        # if the dependency is that of the same noun phrase, it combines calls
        #  itself recursively and combines the results
        if c_dep in NP:
            c_np = find_np_rec(c, conj)

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
                    p_np = find_np_rec(p, conj)
                    
                    # same mapping as the example before except it includes the
                    #  index of the preposition
                    index_list = list(map(lambda l : index_list[0] + [get_index(c)] + l, p_np)) \
                        + index_list[1:]
        # if the dependency is either a conjunction or an appositive, it finds
        #  the noun phrase of that word and adds it to the end of index_list
        elif conj and (c_dep in CONJ):
            index_list += find_np_rec(c, conj)

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

'''
Function that finds the head conjunction of a token
'''
def find_conj_head(token):
    head = get_head(token)
    while get_dep(head) in CONJ:
        head = get_head(head)
    return head

'''
Function that checks if the token is a verb
'''
def is_verb(token):
    if get_pos(token) in VERB:
        return True
    return False

'''
Function that checks if the token is a noun
'''
def is_noun(token):
    if get_pos(token) in NOUN or get_pos(token) in NUM:
        return True
    return False

'''
Function that checks if a verb token is passive
'''
def is_passive(token):
    # checks if any children are passive
    for c in get_children(token):
        c_dep = get_dep(c)
        if (c_dep in NSUBJPASS) or (c_dep in AUXPASS):
            return True
        
    # if it's used in conjunction with another verb, it checks that verb
    if get_dep(token) in CONJ:
        return is_passive(get_head(token))
    
    return False

'''
Function that checks if a token is an infinitive
'''
def is_infinitive(token):
    if not is_verb(token):
        return False
    
    doc = get_doc(token)
    left = get_token(doc, get_index(token) - 1)

    # checks if the left token is an auxiliary verb equal to "to"
    if get_dep(left) in AUX and get_text(left).upper() == "TO":
        return True
        
    return False

'''
Function that checks if a token is an auxiliary "be" or "have" verb
'''
def is_aux_be_have(token):
    if is_verb(token):
        lemma = get_lemma(token)
        if lemma in AUX_BE or lemma in AUX_HAVE:
            return True
    return False

'''
Function that finds the lemma and tries to match it's capitalization
'''
def find_lemma(token):
        lemma = get_lemma(token)
        v_text = get_text(token)

        if lemma in AUX_BE:
            lemma = "be"
        elif lemma in AUX_HAVE:
            lemma = "have"

        if LEMMA_MATCH_CASE:
            # makes sure that the base form matches the capitalization of the verb
            if v_text.isupper():
                lemma = lemma.upper()
            elif not v_text.islower():
                lemma = lemma.capitalize()

        return lemma
