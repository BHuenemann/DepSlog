from settings import *
import copy





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
