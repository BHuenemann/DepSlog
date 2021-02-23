from settings import *
from helpers import *
from output import *





'''
CASES:
1.  <subj> passive_verb
14. passive_verb prep <np>
'''
def base_passive(token, focus_arg = None):
    if not is_verb(token) or not is_passive(token):
        return

    focus = token if focus_arg is None else focus_arg
    aux = is_aux_be_have(token)

    for c in get_children(focus):
        c_dep = get_dep(c)
        
        if c_dep in NSUBJPASS:
            if aux:
                continue
            
            subj = find_np(c)
            vp = find_vp(token)
            
            write_pattern(1, subj, vp)
            
        elif c_dep in PREP and focus == token:
            for pc in get_children(c):
                p_dep = get_dep(pc)
                if p_dep in POBJ:
                    vp = find_vp(token)
                    prep = [get_text(c)]
                    np = find_np(pc)
                    
                    write_pattern(14, np, vp, prep)
                    
    if get_dep(focus) in CONJ:
        head_conj = find_conj_head(focus)
        base_active(token, head_conj)

'''
CASES:
2.  <subj> active_verb
3.  <subj> active_verb dobj
7.  active_verb <dobj>
13. active_verb prep <np>
'''
def base_active(token, focus_arg = None):
    if not is_verb(token) or is_passive(token):
        return

    focus = token if focus_arg is None else focus_arg
    aux = is_aux_be_have(token)
    subj_found = None
    dobj_found = None
    
    for c in get_children(focus):
        c_dep = get_dep(c)
        
        if c_dep in NSUBJ:
            if aux:
                continue
            
            subj = find_np(c)
            vp = find_vp(token)
            
            write_pattern(2, subj, vp)
            if dobj_found is not None:
                dobj = find_conj_text(dobj_found)
                
                write_pattern(3, subj, vp, dobj)
                
            subj_found = c
            
        elif c_dep in DOBJ and focus == token:
            if aux:
                continue
            
            vp = find_vp(token)
            dobj_np = find_np(c)
            
            write_pattern(7, dobj_np, vp)

            if subj_found is not None:
                subj = find_np(subj_found)
                dobj = find_conj_text(c)
                
                write_pattern(3, subj, vp, dobj)
                
            dobj_found = c
            
        elif c_dep in PREP and focus == token:
            for pc in get_children(c):
                p_dep = get_dep(pc)
                if p_dep in POBJ:
                    vp = find_vp(token)
                    prep = [get_text(c)]
                    np = find_np(pc)
                    
                    write_pattern(13, np, vp, prep)

    if get_dep(focus) in CONJ:
        head_conj = find_conj_head(focus)
        base_active(token, head_conj)

'''
CASES:
4.  <subj> verb infinitive (Passive)
4.  <subj> verb infinitive (Active)
8.  infinitive <dobj>
9.  verb infinitive <dobj> (Passive)
9.  verb infinitive <dobj> (Active)
12. infinitive prep <np>
'''
def base_inf(token):
    if not is_infinitive(token):
        return

    verb = None
    inf = find_conj_text(token)
    head = get_head(token)
    
    if is_verb(head):
        verb = head
        
        for vc in get_children(head):
            v_dep = get_dep(vc)
            if v_dep in NSUBJ:
                subj = find_np(vc)
                vp = find_vp(verb)

                write_pattern(4, subj, vp, inf, True)
                break
            elif v_dep in NSUBJPASS:
                subj = find_np(vc)
                vp = find_vp(verb)

                write_pattern(4, subj, vp, inf, False)
                break

    for c in get_children(token):
        c_dep = get_dep(c)
        if c_dep in DOBJ:
            dobj_np = find_np(c)

            write_pattern(8, dobj_np, inf)
            if verb is not None:
                vp = find_vp(verb)
                
                if not is_passive(verb):
                    write_pattern(9, dobj_np, vp, inf, True)
                else:
                    write_pattern(9, dobj_np, vp, inf, False)
        elif c_dep in PREP:
            for pc in get_children(c):
                p_dep = get_dep(pc)
                if p_dep in POBJ:
                    prep = [get_text(c)]
                    np = find_np(pc)
                    
                    write_pattern(12, np, inf, prep)

'''
CASES:
5.  <subj> auxbe noun
6.  <subj> auxhave noun
10. noun auxbe <dobj>
11. noun auxhave <dobj>
'''
def base_aux(token):
    if not is_aux_be_have(token):
        return

    lemma = find_lemma(token)
    subj_found = None
    dobj_found = None

    for c in get_children(token):
        c_dep = get_dep(c)
        
        if c_dep in NSUBJ or c_dep in NSUBJPASS:
            if dobj_found is not None:
                subj = find_conj_text(c)
                subj_np = find_np(c)
                dobj = find_conj_text(dobj_found)
                dobj_np = find_np(dobj_found)

                if lemma.lower() in AUX_BE:
                    write_pattern(5, subj_np, [lemma], dobj)
                    write_pattern(10, dobj_np, subj, [lemma])
                elif lemma.lower() in AUX_HAVE:
                    write_pattern(6, subj_np, [lemma], dobj)
                    write_pattern(11, dobj_np, subj, [lemma])
                break
                
            subj_found = c
            
        elif c_dep in DOBJ:
            if subj_found is not None:
                subj = find_conj_text(subj_found)
                subj_np = find_np(subj_found)
                dobj = find_conj_text(c)
                dobj_np = find_np(c)
                
                if lemma.lower() in AUX_BE:
                    write_pattern(5, subj_np, [lemma], dobj)
                    write_pattern(10, dobj_np, subj, [lemma])
                elif lemma.lower() in AUX_HAVE:
                    write_pattern(6, subj_np, [lemma], dobj)
                    write_pattern(11, dobj_np, subj, [lemma])
                break
                
            dobj_found = c

'''
CASES:
15. noun prep <np>
'''
def base_nprep(token):
    if not is_noun(token):
        return

    for c in get_children(token):
        c_dep = get_dep(c)
        
        if c_dep in PREP:
            for pc in get_children(c):
                p_dep = get_dep(pc)
                if p_dep in POBJ:
                    noun = find_conj_text(token)
                    prep = [get_text(c)]
                    np = find_np(pc)
                    
                    write_pattern(15, np, noun, prep)

'''
CASES:
16. premod noun
'''
def base_premod(token):
    if get_dep(token) not in PREMOD or get_pos(token) not in NOUN:
        return

    head = get_head(token)

    write_pattern(16, [get_text(head)], [get_text(token)])

'''
CASES:
17. conj np
'''
def addon_conj(token):
    if get_dep(token) not in CONJ:
        return

    head_conj = find_conj_head(token)
    
    if get_pos(token) not in NOUN or get_pos(head_conj) not in NOUN:
        return

    cur_conj_text = [get_text(token)]
    cur_conj_np = find_np(token, False)
    head_conj_text = [get_text(head_conj)]
    head_conj_np = find_np(head_conj, False)
    
    write_pattern(17, head_conj_np, cur_conj_text)
    write_pattern(17, cur_conj_np, head_conj_text)

'''
CASE:
18. 
'''
