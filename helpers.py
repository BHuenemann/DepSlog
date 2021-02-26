from settings import *





'''
Wrapper function for recursively finding the noun phrase of a token.

First it calls the recusive function and sorts the resulting index
list so that the noun phrase is in order. The 'conj' variable refers
to whether or not it should search for all noun phrases being used
in conjunction with the main phrase.

Then it goes through each list of indices and substitutes the token's
text into them. At the end, it combines the text of each noun phrase

EX. [[2,1,3], [7,8,6,9]] => [[1,2,3], [6,7,8,9]]
                         => [["the","angy","dog"], ["the","giant","rat","monster"]]
                         => ["the angry dog", "the giant rat monster"]

'''
def find_np(token, conj):
    doc = get_doc(token)
    index_list = find_np_rec(token, conj)
    for l in index_list:
        l.sort()

    separator = ' '
    return list(map(lambda l : \
                    separator.join(list(map(lambda i : \
                                            get_text(get_token(doc, i)), l))), index_list))



'''
Recursive function for finding the noun phrase of a token. If the conj
parameter is true, it also finds all of the phrases that are being used
in conjunction.

It starts with the current token's index. Then it goes through the
children of the token to check if they are part of the noun phrase or
related to it (conjunction).

--If the dependency is in the same noun phrase, it calls itself
  recursively and combines the result. The details of this combination
  are in the function but it's main purpose is to copy the beginning of
  the noun phrase to each of the conjunctions that use it.

  EX. "millitary and homeland security department"
      "millitary department" and "homeland security department"

--If the dependency is the prepositional word "of", it searches for a
  prepositional object and then adds that to the noun phrase along with
  the preposition.

--If the dependency is a conjunction and the conj parameter is enabled,
  it finds the noun phrase of that word and adds it to the end of
  index_list

In summary, Each noun phrase is an unsorted list of indices. Whenever
this function encounters an conjunction, it branches into another noun
phrase while keeping track of the modifiers that have been used so far.

Returns a list of all of the noun phrase index lists associated with
the token.
'''
def find_np_rec(token, conj):
    index_list = [[get_index(token)]]

    for c in get_children(token):
        c_dep = get_dep(c)
        
        if c_dep in NP:
            c_np = find_np_rec(c, conj)

            # this takes all adds the first element of index_list to all of the
            #  elements of c_np. Then it takes the result of that to replace the
            #  first element of index_list
            #
            #    EX. index_list = [[30,31,32], [40], [47]]
            #        c_np = [[35,36], [38]]
            #        =>
            #        index_list = [[30,31,32,35,36], [30,31,32,38], [40], [47]]
            #
            index_list = list(map(lambda l : index_list[0] + l, c_np)) + index_list[1:]

        elif (c_dep in PREP) and (get_text(c).upper() == "OF"):
            for p in get_children(c):
                if get_dep(p) in POBJ:
                    p_np = find_np_rec(p, conj)
                    
                    # same mapping as the example before except it includes the
                    #  index of the preposition
                    index_list = list(map(lambda l : index_list[0] + [get_index(c)] + l, p_np)) \
                        + index_list[1:]
        elif conj and (c_dep in CONJ):
            index_list += find_np_rec(c, conj)

    return index_list



'''
Wrapper function for recursively finding the verb phrase of a token.

This is a simpler version of the noun phrase function so refer to
'find_np' for more details.
'''
def find_vp(token):
    doc = get_doc(token)
    index_list = find_vp_rec(token)
    index_list.sort()

    separator = '_'
    return [separator.join(list(map(lambda i : get_text(get_token(doc, i)), index_list)))]



'''
Recursive function for finding the verb phrase of a token.

Again, this is a simpler version of the noun phrase function since it
doesn't deal with conjunctions at all. Refer to 'find_np_rec' for more
detials.

Returns a list of the verb phrase indices.
'''
def find_vp_rec(token):
    index_list = [get_index(token)]
    
    for c in get_children(token):
        c_dep = get_dep(c)
        if c_dep in VP:
            index_list += find_vp_rec(c)
    
    return index_list



'''
Recursive function for finding any conjunctions for a token.

It starts with the current token and iterates through it's children
to look for any conjunctions to add to the list.

Returns a list of conjunctions in token form.
'''
def find_conj(token):
    index_list = [token]

    for c in get_children(token):
        if get_dep(c) in CONJ:
            index_list += find_conj(c)
            
    return index_list



'''
Alternate version of find_conj that converts the tokens into text. This version
is mainly used for writing/printing.
'''
def find_conj_text(token):
    return list(map(lambda t : get_text(t), find_conj(token)))



'''
Function that finds the head conjunction of a token.
'''
def find_conj_head(token):
    head = get_head(token)
    while get_dep(head) in CONJ:
        head = get_head(head)
    return head



'''
Function that checks if the token is a verb.
'''
def is_verb(token):
    if get_pos(token) in VERB:
        return True
    return False



'''
Function that checks if the token is a noun.
'''
def is_noun(token):
    if get_pos(token) in NOUN or get_pos(token) in NUM:
        return True
    return False



'''
Function that checks if a verb token is passive.

It does this by checking the children for any passive nominal subjects
or passive auxiliaries. If the token is being used in conjunction with
another verb and it hasn't found anything, it checks the head verb too.
'''
def is_passive(token):
    if not is_verb(token):
        return False

    for c in get_children(token):
        c_dep = get_dep(c)
        if (c_dep in NSUBJPASS) or (c_dep in AUXPASS):
            return True

    if get_dep(token) in CONJ:
        return is_passive(get_head(token))
    
    return False



'''
Function that checks if a token is an infinitive.

It relies on infinitives having the "xcomp" dependency and their
left token being equal to "to".
'''
def is_infinitive(token):
    if not is_verb(token):
        return False
    
    doc = get_doc(token)
    left = get_token(doc, get_index(token) - 1)

    if get_dep(token) in XCOMP and get_text(left).upper() == "TO":
        return True
        
    return False



'''
Function that checks if a token is an auxiliary "be" or "have" verb.
'''
def is_aux_be_have(token):
    if is_verb(token):
        lemma = get_lemma(token)
        if lemma in AUX_BE or lemma in AUX_HAVE:
            return True
    return False



'''
Function that finds the lemma.

If the setting for matching the lemma case is enabled, it tries to
match the capitalization of the verb.
'''
def find_lemma(token):
        lemma = get_lemma(token)
        v_text = get_text(token)

        if lemma in AUX_BE:
            lemma = "be"
        elif lemma in AUX_HAVE:
            lemma = "have"

        if LEMMA_MATCH_CASE:
            if v_text.isupper():
                lemma = lemma.upper()
            elif not v_text.islower():
                lemma = lemma.capitalize()

        return lemma
