import truecase
import spacy





'''
CONSTANTS
'''
FILE_IN_PATH = "../Texts/"
FILE_TYPE = ""
PRINT_PROGRESS = True
PROGRESS_INTERVAL = 10

TRUE_CASE = True
ENABLE_APPOS = False
COMBINE_CONJ = True
CONJ_SEPARATOR = ":CONJ"

LEMMA_MATCH_CASE = True

STRIP_PUNC = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''

WRITE_TO_FILE = True
CONSOLE_INPUT = False
FILE_OUT = "patterns.cases"





'''
DEPENDENCY LABELS

Acceptable dependencies for each category
'''
NSUBJ = ["nsubj", "expl"]
NSUBJPASS = ["nsubjpass"]
XCOMP = ["xcomp"]
ACOMP = ["acomp"]
AUX = ["aux"]
AUXPASS = ["auxpass"]
AGENT = ["agent"]

DOBJ = ["dobj", "attr"]

VP = ["neg", "prt"]
NP = ["neg", "nmod", "nummod", "advmod", "amod", "poss", "predet", "det", "case", "compound", "dep"]
PREMOD = ["nmod", "advmod", "amod", "compound"]

PREP = ["prep"]
POBJ = ["pobj"]

CONJ_RAW = ["conj"]
APPOS_RAW = ["appos"]
CONJ = CONJ_RAW + APPOS_RAW if ENABLE_APPOS else CONJ_RAW

AUX_BE = ["be", "are"]
AUX_HAVE = ["have"]

ROOT = ["ROOT"]

'''
POS LABELS
'''
NOUN = ["NOUN", "PRON", "PROPN"]
NUM = ["NUM"]
VERB = ["VERB"]





'''
GETTER METHODS
'''
nlp = spacy.load ("en_core_web_lg")
def create_doc(text):
    if TRUE_CASE:
        content = truecase.get_true_case(text).replace('\n', ' ')
    else:
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

def get_pos(token):
    return token.pos_

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
