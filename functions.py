from settings import *
from helpers import *
from output import *





'''
Base function for if the token is a nominal subject.

CASES:
2.  <subj> active_verb
3.  <subj> active_verb dobj
4.  <subj> verb infinitive (Active)
5.  <subj> auxbe noun
6.  <subj> auxhave noun
7.  active_verb <dobj>
9.  verb infinitive <dobj>
10. noun auxbe <dobj>
11. noun auxhave <dobj>
'''
def base_nsubj(token):
    # checks if the head of the token is a nominal subject
    if get_dep(token) not in NSUBJ:
        return

    # extracts the document, head verb, the noun phrase containing the subject
    #  to use later, a list of verbs that are used in conjunction with the
    #  head verb
    doc = get_doc(token)
    head_verb = get_head(token)
    subj = find_np(token)
    vp_conj = find_conj(head_verb)

    # iterates through each of the conjunction verbs to check for patterns
    for verb in vp_conj:
        # extracts the base form of the verb, it's text, and the verb phrase
        lemma = get_lemma(verb)
        v_text = get_text(verb)
        vp = find_vp(verb)

        # makes sure that the base form matches the capitalization of the verb
        if v_text.isupper():
            lemma = lemma.upper()
        elif not v_text.islower():
            lemma = lemma.capitalize()

        # if the verb's base form is "be" or "have", it checks for any direct
        #  objects under the verb for cases 5, 6, 10, and 11
        if lemma.upper() == "BE" or lemma.upper == "HAVE":
            found_dobj = False
            for verbc in get_children(verb):
                if get_dep(verbc) in DOBJ:
                    # extracts any other direct objects used in conjunction with
                    #  the direct object and the noun phrase of the direct object
                    dobj = find_conj_text(verbc)
                    dobj_np = find_np(verbc)
                    noun = find_conj_text(token)

                    # uses this information to record patterns depending on if it's
                    #  "be" or "have"
                    if lemma.upper() == "BE":
                        write_pattern(5, subj, [lemma], dobj)
                        write_pattern(10, dobj_np, [lemma], noun)
                    else:
                        write_pattern(6, subj, [lemma], dobj)
                        write_pattern(11, dobj_np, [lemma], noun)
                        
                    found_dobj = True
                    break

                
            # if it found a direct object, it continues with the next verb.
            #  Otherwise, it uses the information to create a pattern for
            #  case 2
            if found_dobj:
                continue
            write_pattern(2, subj, vp)

        # otherwise it records case 2 and checks for cases 3, 4, 7, and 9 
        else:
            write_pattern(2, subj, vp)
            for verbc in get_children(verb):
                verbc_dep = get_dep(verbc)

                # if the verb has a direct object, it finds other direct objects
                #  used in conjunction with the direct object and it records the
                #  relevant patterns
                if verbc_dep in DOBJ:
                    dobj = find_conj_text(verbc)
                    dobj_np = find_np(verbc)
                    
                    write_pattern(3, subj, vp, dobj)
                    write_pattern(7, dobj_np, vp)
                # if the verb has an open clausal complement, it checks to see if
                #  that word fits the form of an infinitive by seeing if the left
                #  word before it is "to"
                elif verbc_dep in XCOMP:
                    left = get_token(doc, get_index(verbc) - 1)
                    if get_text(left).upper() == "TO":
                        # if it is an infinitive, it extracts all potential
                        #  conjunctions and checks for direct objects under the
                        #  infinitive
                        inf = find_conj_text(verbc)
                        
                        for verbcc in get_children(verbc):
                            if get_dep(verbcc) in DOBJ:
                                dobj_np = find_np(verbcc)
                                
                                write_pattern(9, dobj_np, vp, inf, True)
                                break
                        write_pattern(4, subj, vp, inf, True)
    
'''
Nominal Subject (Passive)
CASES:
1.  <subj> passive_verb
4.  <subj> verb infinitive (Passive)
9.  verb infinitive <dobj> (Passive)
'''
def base_nsubjpass(token):
    # checks if the head of the token is a passive voice nominal subject
    if get_dep(token) not in NSUBJPASS:
        return

    # extracts the document, head verb, the noun phrase containing the subject
    #  to use later, a list of verbs that are used in conjunction with the
    #  head verb
    doc = get_doc(token)
    head_verb = get_head(token)
    subj = find_np(token)
    vp_conj = find_conj(head_verb)

    # iterates though the conjunction verbs to record the passive verb pattern
    #  and check for any infinitives
    for verb in vp_conj:
        vp = find_vp(verb)
        write_pattern(1, subj, vp)
        
        for verbc in get_children(verb):
            # if the verb has an open clausal complement, it checks to see if
            #  that word fits the form of an infinitive by seeing if the left
            #  word before it is "to"
            if get_dep(verbc) in XCOMP:
                left = get_token(doc, get_index(verbc) - 1)
                if get_text(left).upper() == "TO":
                    # if it is an infinitive, it extracts all potential
                    #  conjunctions and checks for direct objects under the
                    #  infinitive
                    inf = find_conj_text(verbc)
                
                    for verbcc in get_children(verbc):
                        if get_dep(verbcc) in DOBJ:
                            dobj_np = find_np(verbcc)
                        
                            write_pattern(9, dobj_np, vp, inf, False)
                            break
                    write_pattern(4, subj, vp, inf, False)

'''
Direct Object
CASES:
8.  infinitive <dobj>
'''
def base_dobj(token):
    # checks if the head of the token is a direct object
    if get_dep(token) not in DOBJ:
        return

    # extracts the document, head verb, and a list of verbs that are used in
    #  conjunction with the head verb
    doc = get_doc(token)
    head_verb = get_head(token)
    vp_conj = find_conj(head_verb)

    # iterates through the conjunction verbs to check for any infinitives
    for verb in vp_conj:
        left = get_token(doc, get_index(verb) - 1)
        if get_text(left).upper() == "TO":
            # extracts the noun phrase of the direct object and the verb phrase
            #  of the verb and then records the pattern
            dobj_np = find_np(token)
            vp = find_vp(verb)
        
            write_pattern(8, dobj_np, vp)
            
'''
Preposition
CASES:
12. infinitive prep <np>
13. active_verb prep <np>
14. passive_verb prep <np>
15. noun prep <np>
'''
def base_pobj(token):
    # checks if the head of the token is a prepositional object
    if get_dep(token) not in POBJ:
        return

    # extracts the preposition and the head verb
    prep = get_head(token)
    head_verb = get_head(prep)

    # if the preposition is equal to the head verb, there is nothing to extract
    #  so it returns
    if prep == head_verb:
        return

    # extracts the document, the prepositional object's noun phrase, the
    #  preposition's text, the word to the left of the head verb, and
    #  a list of verbs that are used in conjunction with the head verb
    doc = get_doc(token)
    np = find_np(token)
    prep_text = [get_text(prep)]
    left = get_token(doc, get_index(head_verb) - 1)
    vp_conj = find_conj(head_verb)

    # iterates through the conjunction verbs to check for infinitives and
    #  nominal subjects
    for verb in vp_conj:
        found_out = False

        # checks if the verb is an infinitive
        if get_text(left).upper() == "TO":
            # extracts the verb phrase and then records the pattern
            vp = find_vp(head_verb)
            write_pattern(12, np, vp, prep_text)
            found_out = True

        # iterates through all of the verb's children to check if any are
        #  nominal subjects
        for verbc in get_children(verb):
            verbc_dep = get_dep(verbc)

            # if it finds any, it extracts the verb phrase and records the
            #  pattern
            if verbc_dep in NSUBJ:
                vp = find_vp(verb)
                write_pattern(13, np, vp, prep_text)
                found_out = True
            elif verbc_dep in NSUBJPASS:
                vp = find_vp(verb)
                write_pattern(14, np, vp, prep_text)
                found_out = True

        # if it hasn't recorded any patterns so far, it assumes that the
        #  verb was actually a noun and records that pattern
        if not found_out:
            noun = [get_text(verb)]
            write_pattern(15, np, noun, prep_text)
