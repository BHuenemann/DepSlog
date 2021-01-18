import spacy





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
