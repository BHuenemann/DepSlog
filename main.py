from pathlib import Path
from functions import *




FILE_PATH = "../Texts/"
FILE_NAME = "DEV-MUC3-"
FILE_OUT = "patterns.cases"

MULT_FILES = True
FILE_START = 1
FILE_END = 1              #1300
FILL_DIGITS = True
DIGIT_COUNT = 4

WRITE_TO_FILE = True
DISPLACY = False





OUT_FILE = open(FILE_OUT, "w")

for i in range(FILE_START, FILE_END + 1):
    file_num = ""
    if MULT_FILES and FILL_DIGITS:
        file_num = str(i).zfill(DIGIT_COUNT)
    elif MULT_FILES:
        file_num = str(i)
        
    file_to_open = Path(FILE_PATH + FILE_NAME + file_num)
    f = open(file_to_open, 'r')
    text = f.read()

    doc = create_doc(text)

    for sent in get_sents(doc):
        for token in sent:
            dep = get_dep(token)
            if dep in NSUBJ:
                nsubj(token)
            elif dep in NSUBJPASS:
                nsubjpass(token)
            elif dep in DOBJ:
                dobj(token)
            elif dep in POBJ:
                pobj(token)
                          
    f.close()

    if not MULT_FILES:
        break
    
OUT_FILE.close()

if DISPLACY:
    displacy.serve(doc, style="dep")
