from settings import *
from helpers import *
from output import *





'''
Basic function that handles passive verb patterns. It returns immediately
if the token is not a passive verb since then there are no patterns to
report.

This function looks for the children of the focus to look for any passive
nominal subjects or any prepositions. If it finds these, it extracts the
necessary information and writes the patterns.

For prepositions, it extracts the information by looking for any
prepositional objects that depend on the preposition.

It also checks at the beginning to make sure that the token is not an
auxiliary so it doesn't overlap with the other base functions. If the token
is an auxiliary, it will still do the search but only report preposition
patterns.

This function optionally takes in a separate token to focus on. The method
looks for subject patterns under the focus but then still prints the patterns
with the token verb as the passive_verb. This functionality allows for a
verb that's part of a conjunction chain to look for any patterns from the
head conjunction.

EX. "He jumped and ran."
    
    base_passive(ran, jumped)
      => writes "He * <subj>_passive_verb__ran"

    This allows it to extract patterns that don't immediately pertain to
    the input token but should still be extracted.

It also doesn't look for any prepositions under the focus verb if the
focus verb is different from the regular verb. This is because prepositions
of head conjunctions usually don't apply to the other verbs.

At the end, it checks if the verb is part of a conjunction chain and if so,
it calls itself with the head conjunction as the focus to get any related
patterns.

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
            
            subj = find_np(c, True)
            vp = find_vp(token)
            
            write_pattern(1, subj, vp)
            
        elif c_dep in PREP and focus == token:
            for pc in get_children(c):
                p_dep = get_dep(pc)
                if p_dep in POBJ:
                    vp = find_vp(token)
                    prep = [get_text(c)]
                    np = find_np(pc, True)
                    
                    write_pattern(14, np, vp, prep)
                    
    if get_dep(focus) in CONJ:
        head_conj = find_conj_head(focus)
        base_active(token, head_conj)

'''
Basic function that handles active verb patterns. It returns immediately
if the token is not an active verb since then there are no patterns to
report.

This function inputs a focus token in the same way that the function
'base_passive' does. Refer to the documentation on that function for
details on this.

First, this function searches for nominal subject and preposition patterns.
While it does this, it adds each subject to a list so that it can use that
list for direct object patterns later. It handles prepositions in the same
way that 'base_passive' does

Then when it is done going through for those patterns, it goes through the
same tokens a second time if the focus is different from the token and the
token is not an auxiliary. This time, it looks for direct objects and then
writes patterns for those objects with all of the subjects found in the
previous loop.

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
    subj_list = []

    # first loop to look for nominal subjects and prepositions
    for c in get_children(focus):
        c_dep = get_dep(c)
        
        if c_dep in NSUBJ:
            if aux:
                continue
            
            subj = find_np(c, True)
            vp = find_vp(token)
            
            write_pattern(2, subj, vp)
                
            subj_list += [c]
            
        elif c_dep in PREP and focus == token:
            for pc in get_children(c):
                p_dep = get_dep(pc)
                if p_dep in POBJ:
                    vp = find_vp(token)
                    prep = [get_text(c)]
                    np = find_np(pc, True)
                    
                    write_pattern(13, np, vp, prep)

    # second loop to look for direct objects
    if focus == token and not aux:
        for c in get_children(focus):
            c_dep = get_dep(c)
            if c_dep in DOBJ:
                vp = find_vp(token)
                dobj_np = find_np(c, True)
            
                write_pattern(7, dobj_np, vp)

                for subj_token in subj_list:
                    subj = find_np(subj_token, True)
                    dobj = find_conj_text(c)
                
                    write_pattern(3, subj, vp, dobj)

    if get_dep(focus) in CONJ:
        head_conj = find_conj_head(focus)
        base_active(token, head_conj)

'''
CASES:
Basic function that handles infinitive patterns. It returns immediately
if the token is not an infinitive since then there are no patterns to
report.

First, this method checks if the head of the infinitive is a verb. This
will be usefull for patterns 4 and 9. If it is a verb, the function
searches for any subjects attached to that verb and prints those patterns
under pattern 4. It also keeps track of the verb in case it finds a
direct object later for pattern 9.

Then it goes through the children of the infinitive to look for direct
objects or prepositions. If it finds a direct object, it checks to see
if it found a verb as the head from earlier and uses that to print
pattern 9. Prepositions are handled the same as the previous functions.

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
                subj = find_np(vc, True)
                vp = find_vp(verb)

                write_pattern(4, subj, vp, inf, True)
            elif v_dep in NSUBJPASS:
                subj = find_np(vc, True)
                vp = find_vp(verb)

                write_pattern(4, subj, vp, inf, False)

    for c in get_children(token):
        c_dep = get_dep(c)
        if c_dep in DOBJ:
            dobj_np = find_np(c, True)

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
                    np = find_np(pc, True)
                    
                    write_pattern(12, np, inf, prep)

'''
Basic function that handles auxiliary verb patterns. It returns immediately
if the token is not an auxiliary verb since then there are no patterns to
report.

All of the patterns that this function is looking for involve both a subject
and a direct object. It handles these in the same way that the function
'base_active' does. This is done by searching through the children for all
of the nominal subjects or passive nominal subjects first. Then it iterates
again to look for direct objects. Refer to the documentation on 'base_active'
for more details on this.

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
    subj_list = []

    # first loop
    for c in get_children(token):
        c_dep = get_dep(c)
        
        if c_dep in NSUBJ or c_dep in NSUBJPASS:
            subj_list += [c]

    # second loop
    for c in get_children(token):
        c_dep = get_dep(c)
        if c_dep in DOBJ:
            for subj_token in subj_list:
                subj = find_conj_text(subj_token)
                subj_np = find_np(subj_token, True)
                dobj = find_conj_text(c)
                dobj_np = find_np(c, True)
                
                if lemma.lower() in AUX_BE:
                    write_pattern(5, subj_np, [lemma], dobj)
                    write_pattern(10, dobj_np, subj, [lemma])
                elif lemma.lower() in AUX_HAVE:
                    write_pattern(6, subj_np, [lemma], dobj)
                    write_pattern(11, dobj_np, subj, [lemma])

'''
Basic function that handles noun preposition patterns. It returns immediately
if the token is not a noun since then there are no patterns to report.

After identifying the token as a noun, it searches through the chilren to look
for any preposition patterns. This uses the same extraction method for
prepositions as previous functions.

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
                    np = find_np(pc, True)
                    
                    write_pattern(15, np, noun, prep)

'''
Basic function that handles pre-modifier patterns. It returns immediately
if the token is not a noun premodifier since then there are no patterns to
report.

CASES:
16. premod noun
'''
def base_premod(token):
    if get_dep(token) not in PREMOD or get_pos(token) not in NOUN:
        return

    head = get_head(token)

    write_pattern(16, [get_text(head)], [get_text(token)])

'''
Additional function that handles conjunction patterns. It returns immediately
if the token is not a conjunction since then there are no patterns to report.

It searches for the head conjunction and then returns if either tokens are
not nouns. Then it writes two patterns for those conjunctions that are
in reverse order from each other.

CASES:
17. NPConj <np>
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
Additional function that handles predicate adjectives. It returns immediately
if the token is not an adjectival complement since then there are no patterns
to report.

Then it assumes that the head of that token is a verb and it searches for any
nominal subjects or passive nominal subjects related to that verb. If it finds
any subjects, it writes them in a pattern.

CASE:
18. <subj> PredAdj
'''
def addon_predadj(token):
    if get_dep(token) not in ACOMP:
        return

    pred_adj = [get_text(token)]
    verb = get_head(token)

    for c in get_children(verb):
        c_dep = get_dep(c)
        if c_dep in NSUBJ or c_dep in NSUBJPASS:
            subj = find_np(c, True)
            write_pattern(18, subj, pred_adj)
