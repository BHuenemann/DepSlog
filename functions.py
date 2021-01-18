from settings import *
from helpers import *
from output import *





'''
Nominal Subjects

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
def nsubj(token):
    doc = get_doc(token)
    head_verb = get_head(token)
    subj = find_np(token)
    vp_conj = find_conj(head_verb)

    for verb in vp_conj:
        lemma = get_lemma(verb)
        v_text = get_text(verb)
        if v_text.isupper():
            lemma = lemma.upper()
        elif not v_text.islower():
            lemma = lemma.capitalize()
            
        vp = find_vp(verb)
        
        if lemma.upper() == "BE":
            found_dob = False
            for verbc in get_children(verb):
                if get_dep(verbc) in DOBJ:
                    dobj = find_conj_text(verbc)
                    dobj_np = find_np(verbc)
                    noun = find_conj_text(token)
                    
                    write_pattern(5, subj, [lemma], dobj)
                    write_pattern(10, dobj_np, [lemma], noun)
                    found_dob = True
                    break
            if found_dob:
                continue
            write_pattern(2, subj, vp)
        elif lemma.upper == "HAVE":
            found_dob = False
            for verbc in get_children(verb):
                if get_dep(verbc) in DOBJ:
                    dobj = find_conj_text(verbc)
                    dobj_np = find_np(verbc)
                    noun = find_conj_text(token)
                            
                    write_pattern(6, subj, [lemma], dobj)
                    write_pattern(11, dobj_np, [lemma], noun)
                    found_dob = True
                    break
            if found_dob:
                continue
            write_pattern(2, subj, vp)
        else:
            write_pattern(2, subj, vp)
            for verbc in get_children(verb):
                verbc_dep = get_dep(verbc)
                                
                if verbc_dep in DOBJ:
                    dobj = find_conj_text(verbc)
                    dobj_np = find_np(verbc)
                    
                    write_pattern(3, subj, vp, dobj)
                    write_pattern(7, dobj_np, vp)
                elif verbc_dep in XCOMP:
                    left = get_token(doc, get_index(verbc) - 1)
                    if get_dep(left) in AUX and get_text(left).upper() == "TO":
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
def nsubjpass(token):
    head_verb = get_head(token)
    subj = find_np(token)
    vp_conj = find_conj(head_verb)

    for verb in vp_conj:
        vp = find_vp(verb)
        for verbc in get_children(verb):
            if get_dep(verbc) in XCOMP:
                left = get_token(doc, get_index(verbc) - 1)
                if get_dep(left) in AUX and get_text(left).upper() == "TO":
                    inf = find_conj_text(verbc)
                
                    for verbcc in get_children(verbc):
                        if get_dep(verbcc) in DOBJ:
                            dobj_np = find_np(verbcc)
                        
                            write_pattern(9, dobj_np, vp, inf, False)
                            break
                    write_pattern(4, subj, vp, inf, False)
        write_pattern(1, subj, vp)

'''
Direct Object
CASES:
8.  infinitive <dobj>
'''
def dobj(token):
    doc = get_doc(token)
    verb = get_head(token)
    left = get_token(doc, get_index(verb) - 1)
    if get_dep(left) in AUX and get_text(left).upper() == "TO":
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
def pobj(token):
    doc = get_doc(token)
    prep = get_head(token)
    prep_head = get_head(prep)
    if prep == prep_head:
        return
    
    np = find_np(token)
    prep_text = [get_text(prep)]
    found_out = False
    is_obj = True

    left = get_token(doc, get_index(prep_head) - 1)
    if get_dep(left) in AUX and get_text(left).upper() == "TO":
        vp = find_vp(prep_head)
        write_pattern(12, np, vp, prep_text)
        found_out = True
    
    for verbc in get_children(prep_head):
        verbc_dep = get_dep(verbc)
        
        if verbc_dep in NSUBJ:
            vp = find_vp(prep_head)
            write_pattern(13, np, vp, prep_text)
            found_out = True
        elif verbc_dep in NSUBJPASS:
            vp = find_vp(prep_head)
            write_pattern(14, np, vp, prep_text)
            found_out = True

    if not found_out:
        noun = [get_text(prep_head)]
        write_pattern(15, np, noun, prep_text)
