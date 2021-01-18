import spacy
from spacy import displacy
from pathlib import Path

nlp = spacy.load ("en_core_web_sm")

text_folder = Path("Texts/")
file_to_open = text_folder / "DEV-MUC3-0001"

f = open(file_to_open, 'r')
text = f.read()
#content = text.replace('\n', ' ')
content = "The car bought by John is red. The car was bought by John."

doc = nlp(content)





def PrintPattern(np, n_relation, d_relation, d_word, d_mod = '', is_rev = False):
        np_pp = IncludePP(np)
        #np_pp = np
        
        d_phrase, has_dob = IncludeDob(d_word)
        dob = "_Dobj" if has_dob else ''

        if has_dob:
                structure = " * " + d_relation + "_<" +  n_relation + ">__" if is_rev \
                        else " * <" + n_relation + ">_" + d_relation + "__"
                print(np_pp.text + structure + d_mod + d_word.text)

        if not n_relation == "dobj":
                structure = " * " + d_relation + "_<" +  n_relation + ">__" if is_rev \
                        else " * <" + n_relation + ">_" + d_relation + dob + "__"
                print(np_pp.text + structure + d_mod + d_phrase.text)

def PunctClearList(np, obj_list):
        if np.doc[np.end + 1].pos_ == "SPACE":
                obj_list.clear()




                
def FindConj(np, token, obj_list):
        for t in token.head.children:
                if t.dep_ == "conj":
                        if t.left_edge.dep_ == "auxpass" or t.left_edge.dep == "nsubjpass":
                                PrintPattern(np, "subj", "PassVP", t)
                        else:
                                PrintPattern(np, "subj", "ActVP", t)

def FindAppos(np, token, obj_list):
        for t in token.children:
                if t.dep_ == "appos":
                        ProcessNP(np, t, token.head, obj_list)

def FindRelCl(np, token):
        noun = np[len(np) - 1]
        for t in noun.children:
                if t.dep_ == "relcl":
                        if t.left_edge.dep_ == "auxpass" or t.left_edge.dep_ == "nsubjpass":
                                PrintPattern(IncludeNP(token), "subj", "PassVP", t)
                        else:
                                PrintPattern(IncludeNP(token), "subj", "ActVP", t)




                                
def IncludePP(np):
        token = np[len(np) - 1]
        end = np.end + 1
        
        for t in token.children:
                if t.dep_ == "prep":
                        end = t.right_edge.i + 1 if t.right_edge.i  + 1 > end else end

        if np.doc[end - 1].text == '.' or ',':
                end -= 1
        return np.doc[np.start : end]
                                
def IncludeNP(token):
        start = token.i
        for t in token.children:
                if t.dep_ == "compound" or t.dep_ == "det" or t.dep == "nmod":
                        start = t.i if t.i < start else start
        return token.doc[start : token.i + 1]

def IncludeDob(token):
        for t in token.children:
                if t.dep_ == "dobj":
                        return token.doc[token.i : t.i + 1], True
        return token, False





def IsInfinitive(token):
        for t in token.children:
                if t.dep_ == "aux" and t.text.upper() == "TO":
                        return True
        return False





def ProcessHaveBeen(token):
        verb = None
        have = False
        for t in token.children:
                if t.dep_ == "attr" or t.dep_ == "acomp":
                        verb = t
                elif t.dep_ == "aux" and t.text.upper() == "HAVE":
                        have = True

        if not have or verb is None:
                return None
        return verb
        
def ProcessPass(np, token, head, obj_list):
        if head.text.upper() == "BEEN":
                verb = ProcessHaveBeen(head)
                if verb is None:
                        return
                PrintPattern(np, "subj", "PassVP", verb)
                FindConj(np, verb, obj_list)
                
        elif head.text.upper() == "WERE" or head.text.upper() == "WAS":
                for t in head.children:
                        if t.dep_ == "attr" or t.dep_ == "acomp":
                                PrintPattern(np, "subj", "PassVP", t)
                                FindConj(np, t, obj_list)
        return





def ProcessPrepVP(np, token, head, obj_list):
        if head.head.text.upper() == "BEEN":
                verb = ProcessHaveBeen(head.head)
                if verb is not None:
                        PrintPattern(np, "NP", "PassVp_Prep", head, verb.text + ' ', True)
        elif head.head.text.upper() == "WERE" or head.head.text.upper() == "WAS":
                for t in head.head.children:
                        if t.dep_ == "attr" or t.dep_ == "acomp":
                                PrintPattern(np, "NP", "PassVp_Prep", head, t.text + ' ', True)
                                break
        else:
                d_mod = IncludeNP(head.head)
                PrintPattern(np, "NP", "ActVp_Prep", head, d_mod.text + ' ', True)

        for t in token.children:
                if t.dep_ == "prep" and t.text == "IN":
                        return
        if not head.text.upper() == "IN":
                obj_list.append(np)
                
def ProcessPrepNP(np, token, head, obj_list):
        d_mod = IncludeNP(head.head)
        PrintPattern(np, "NP", "Np_Prep", head, d_mod.text + ' ', True)
        
        for t in token.children:
                if t.dep_ == "prep" and t.text == "IN":
                        return
        if not head.text.upper() == "IN":
                obj_list.append(np)




                
def ProcessNSubj(np, token, head, obj_list):
        ProcessPass(np, token, head, obj_list)
        if head.is_stop or token.is_stop:
                return
        PrintPattern(np, "subj", "ActVP", head)
        FindConj(np, token, obj_list)

def ProcessNSubjPass(np, token, head, obj_list):
        if head.is_stop or token.is_stop:
                return
        PrintPattern(np, "subj", "PassVP", head)
        FindConj(np, token, obj_list)

def ProcessPObj(np, token, head, obj_list):
        if head == head.head or (token.is_stop and len(np) == 1):
                return
        elif head.head.pos_ == "VERB":
                ProcessPrepVP(np, token, head, obj_list)
        else:
                ProcessPrepNP(np, token, head, obj_list)
                
        if head.text.upper() == "IN":
                for np_obj in obj_list:
                        PrintPattern(np, "NP", "NP_Prep", head, np_obj.text + ' ', True)
                obj_list.clear()

def ProcessDObj(np, token, head):
        if IsInfinitive(head):
                PrintPattern(np, "dobj", "infinitive_verb", head, '', True)




                
def ProcessNP(np, token, head, obj_list):
        if token.dep_ == "nsubj":
                ProcessNSubj(np, token, head, obj_list)
        elif token.dep_ == "nsubjpass":
                ProcessNSubjPass(np, token, head, obj_list)
        elif token.dep_ == "pobj":
                ProcessPObj(np, token, head, obj_list)
        elif token.dep_ == "dobj":
                ProcessDObj(np, token, head)
        else:
                PunctClearList(np, obj_list)
                return
        
        PunctClearList(np, obj_list)
        FindRelCl(np, token)
        FindAppos(np, token, obj_list)

for token in doc:
        print(token.text + " ")
        print(token.dep_)

#obj_list = []
#for np in doc.noun_chunks:
#        token = np[len(np) - 1]
#        ProcessNP(np, token, token.head, obj_list)
                        


f.close()
                        
displacy.serve(doc, style="dep")
