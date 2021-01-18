import spacy
from spacy import displacy
from pathlib import Path
import copy





'''
CONSTANTS
'''
TAGS = [1] * 15

FILE_START = 1
FILE_END = 1300              #1300
FILE_DIGITS = 4
FILE_PATH = "Texts/"
FILE_NAME = "DEV-MUC3-"

OUT_FILE = open("patterns.cases", "w")

WRITE_TO_FILE = True
WRITE = OUT_FILE.write if WRITE_TO_FILE else print
DISPLACY = False





'''
DEPENDENCY LABELS
'''
NSUBJ = ["nsubj", "expl"]
NSUBJPASS = ["nsubjpass"]
XCOMP = ["xcomp"]
AUX = ["aux", "auxpass"]
AGENT = ["agent"]

DOBJ = ["dobj", "attr"]

VP = ["neg", "prt"]
NP = ["nmod", "nummod", "advmod", "amod", "poss", "predet", "det", "case", "compound"]

PREP = ["prep"]
POBJ = ["pobj"]

APPOS = ["appos"]
CONJ = ["conj"]





'''
GETTER METHODS
'''
def create_doc(text):
    nlp = spacy.load ("en_core_web_sm")
    content = text.replace('\n', ' ')
    return nlp(content)

def get_doc(token):
    return token.doc

def get_token(doc, index):
    return doc[index]

def get_sents(doc):
    return doc.sents

def get_np(doc):
    return doc.noun_chunks

def get_root(span):
    return span.root

def get_dep(token):
    return token.dep_

def get_head(token):
    return token.head

def get_children(token):
    return token.children

def get_text(token):
    return token.text

def get_lemma(token):
    return token.lemma_

def get_index(token):
    return token.i





'''
WRITE PATTERN:
1.  <subj> passive_verb
2.  <subj> active_verb
3.  <subj> active_verb dobj
4.  <subj> verb infinitive
5.  <subj> auxbe noun
6.  <subj> auxhave noun

7.  active_verb <dobj>
8.  infinitive <dobj>
9.  verb infinitive <dobj>
10. noun auxbe <dobj>
11. noun auxhave <dobj>

12. infinitive prep <np>
13. active_verb prep <np>
14. passive_verb prep <np>
15. noun prep <np>

16. premod <noun>
'''
def write_pattern(case, outs, p1s, p2s = [""], active = False):
    for out in outs:
        for p1 in p1s:
            for p2 in p2s:
                if 1 <= case <= 15:
                    tag = "_" + str(TAGS[case - 1])
                if case == 1:
                    WRITE(out + " * <subj>_PassVp__" + p1 + tag)
                elif case == 2:
                    WRITE(out + " * <subj>_ActVp__" + p1 + "_" + tag)
                elif case == 3:
                    WRITE(out + " * <subj>_ActVp_Dobj__" + p1 + "_" + p2 + tag)
                elif case == 4:
                    if not active:
                        WRITE(out + " * <subj>_PassInfVp__" + p1 + "_" + p2 + tag)
                    else:
                        WRITE(out + " * <subj>_ActInfVp__" + p1 + "_" + p2 + tag)
                elif case == 5 or case == 6:
                    WRITE(out + " * <subj>_AuxVp_Dobj__" + p1 + "_" + p2 + tag)
                elif case == 7:
                    WRITE(out + " * ActVp_<dobj>__" + p1 + tag)
                elif case == 8:
                    WRITE(out + " * infinitive_verb_<dobj>__" + p1 + tag)
                elif case == 9:
                    if not active:
                        WRITE(out + " * PassInfVp_<dobj>__" + p1 + "_" + p2 + tag)
                    else:
                        WRITE(out + " * ActInfVp_<dobj>__" + p1 + "_" + p2 + tag)
                elif case == 10 or case == 11:
                    WRITE(out + " * Subj_AuxVp_<dobj>__" + p1 + "_" + p2 + tag)
                elif case == 12:
                    WRITE(out + " * InfVp_Prep_<NP>__" + p1 + "_" + p2 + tag)
                elif case == 13:
                    WRITE(out + " * ActVp_Prep_<NP>__" + p1 + "_" + p2 + tag)
                elif case == 14:
                    WRITE(out + " * PassVp_Prep_<NP>__" + p1 + "_" + p2 + tag)
                elif case == 15:
                    WRITE(out + " * Np_Prep_<NP>__" + p1 + "_" + p2 + tag)
                elif case == 16:
                    WRITE(out + " * " + p1 + "_premod")

                if 1 <= case <= 15:
                    TAGS[case - 1] += 1

                if WRITE_TO_FILE:
                    WRITE("\n")





'''
HELPER METHODS
'''
def find_np(token):
    doc = get_doc(token)
    index_list = find_np_rec(token, [[]], 0)
    for l in index_list:
        l.sort()

    separator = ' '
    return list(map(lambda l : \
                    separator.join(list(map(lambda i : get_text(get_token(doc, i)), l))), index_list))
    
def find_np_rec(token, index_list, np_num):
    new_list = copy.deepcopy(index_list)
    new_list[np_num].append(get_index(token))
    
    for c in get_children(token):
        c_dep = get_dep(c)
        if c_dep in NP:
            new_list = find_np_rec(c, new_list, np_num)
        elif c_dep in PREP and (get_text(c).upper() == "OF" or get_text(c).upper() == "FOR"):
            for p in get_children(c):
                if get_dep(p) in POBJ:
                    new_list[np_num].append(get_index(c))
                    new_list = find_np_rec(p, new_list, np_num)
        elif (c_dep in CONJ) or (c_dep in APPOS):
            new_list.append(index_list[np_num])
            new_list = find_np_rec(c, new_list, len(new_list) - 1)
    return new_list

def find_vp(token):
    doc = get_doc(token)
    index_list = find_vp_rec(token, [[]], 0)
    for l in index_list:
        l.sort()
    separator = '_'
    return list(map(lambda l :
                    separator.join(list(map(lambda i :
                                            get_text(get_token(doc, i)), l))), index_list))
    
def find_vp_rec(token, index_list, vp_num):
    index_list[vp_num].append(get_index(token))
    for c in get_children(token):
        c_dep = get_dep(c)
        if c_dep in VP:
            index_list = find_vp_rec(c, index_list, vp_num)
    return index_list

def find_conj_text(token):
    return list(map(lambda t : get_text(t), find_conj(token)))

def find_conj(token):
    for c in get_children(token):
        if get_dep(c) in CONJ:
            return [token] + find_conj(c)
    return [token]





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
    verb = get_head(token)
    left = get_token(doc, get_index(verb) - 1)
    if get_dep(left) in AUX and get_text(left).upper() == "TO":
        dobj_np = find_np(token)
        vp = find_vp(verb)
        
        write_pattern(8, dobj_np, vp)
            
'''
Preposition
CASES:
2.  <subj> active_verb (Agent)
3.  <subj> active_verb dobj (Agent)
12. infinitive prep <np>
13. active_verb prep <np>
14. passive_verb prep <np>
15. noun prep <np>
'''
def pobj(token, obj_list):
    prep = get_head(token)
    prep_head = get_head(prep)
    if prep == prep_head:
        return
    
    np = find_np(token)
    prep_text = [get_text(prep)]
    found_out = (False, None, 0)
    is_obj = True

    left = get_token(doc, get_index(prep_head) - 1)
    if get_dep(left) in AUX and get_text(left).upper() == "TO":
        vp = find_vp(prep_head)
        
        write_pattern(12, np, vp, prep_text)
        found_out = (True, None, (12, vp))
    
    for verbc in get_children(prep_head):
        verbc_dep = get_dep(verbc)
        
        if verbc_dep in NSUBJ:
            vp = find_vp(prep_head)
            
            write_pattern(13, np, vp, prep_text)
            found_out = (True, verbc, (13, vp))
        elif verbc_dep in NSUBJPASS:
            vp = find_vp(prep_head)
            
            write_pattern(14, np, vp, prep_text)
            found_out = (True, verbc, (14, vp))
        elif verbc_dep in PREP and get_text(verbc).upper() == "IN":
            is_obj = False

    if not found_out[0]:
        noun = [get_text(prep_head)]
        
        write_pattern(15, np, noun, prep_text)
        found_out = (True, None, (15, noun))
    elif (get_dep(prep) in AGENT) and (found_out[1] is not None):
        dobj = find_np(found_out[1])
                
        write_pattern(3, np, vp, dobj)
        write_pattern(2, np, vp)
        found_out = (True, None, (13, vp))

    pnoun = [get_text(token)]
    if ((15, pnoun) not in obj_list) \
       and not (get_dep(prep) in PREP and get_text(prep).upper() == "IN"):
        in_list = False
        for c in get_children(token):
            if (get_dep(c) in PREP) and (get_text(c).upper() == "IN"):
                in_list = True
        if not in_list:
            obj_list.append((15, pnoun))
    if found_out[0] and is_obj and (found_out[2] not in obj_list) and (found_out[2] != 0):
        obj_list.append(found_out[2])
    elif prep_text[0].upper() == "IN":
        for obj in obj_list:
            case = obj[0]
            outs = obj[1]
            write_pattern(case, np, outs, prep_text)
        obj_list.clear()
        return





'''
MAIN PROGRAM
'''
for i in range(FILE_START, FILE_END + 1):
    file_to_open = Path(FILE_PATH + FILE_NAME + str(i).zfill(FILE_DIGITS))
    f = open(file_to_open, 'r')
    text = f.read()

    doc = create_doc(text)

    for sent in get_sents(doc):
        obj_list = []
        for token in sent:
            dep = get_dep(token)
            if dep in NSUBJ:
                nsubj(token)
            elif dep in NSUBJPASS:
                nsubjpass(token)
            elif dep in DOBJ:
                dobj(token)
            elif dep in POBJ:
                pobj(token, obj_list)
                          
    f.close()
    
OUT_FILE.close()

if DISPLACY:
    displacy.serve(doc, style="dep")
