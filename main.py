import spacy
from spacy import displacy
from pathlib import Path
from functions import *
from settings import *





# opens the necessary output file to write to
if WRITE_TO_FILE:
    out_file = open(FILE_OUT, "w")

'''
Increments through all input files and calls the pattern functions
'''
PASS_TWICE = 2 if ENABLE_PREMOD else 1
for i in range(0, PASS_TWICE):
    file_end = FILE_START + 1 if TEXT_INPUT else FILE_END + 1
    for j in range(FILE_START, file_end):
        if not TEXT_INPUT:
            # automatically adds a number to the end if there are multiple files
            #  and fills the number with 0s if that setting is active
            file_num = ""
            if MULT_FILES and FILL_DIGITS:
                file_num = str(j).zfill(DIGIT_COUNT)
            elif MULT_FILES:
                file_num = str(j)

            # opens the file to read and creates the document for the dependency
            #  parser
            file_to_open = Path(FILE_IN_PATH + FILE_IN + file_num)
            in_file = open(file_to_open, 'r')
            text = in_file.read()
        
            doc = create_doc(text)
            
        else:
            text = input("Enter a sentence: ")
            doc = create_doc(text)
        
            for sent in get_sents(doc):
                for token in sent:
                    print("\n  " + get_text(token) + \
                          "\n\t" + get_dep(token) + " --- " + get_text(get_head(token)) + \
                          "\n\t" + get_pos(token))
            print("\n")

        # increments through each token and calls the functions to check for
        #  patterns
        for sent in get_sents(doc):
            for token in sent:
                if i == 0:
                    base_passive(token)
                    base_active(token)
                    base_inf(token)
                    base_aux(token)
                    base_nprep(token)
                    addon_conj(token)
                elif i == 1:
                    base_premod(token)

        # closes the file and stops if there's only one input file
        if not TEXT_INPUT:
            in_file.close()

        if not MULT_FILES:
            break

displacy.serve(doc, style="dep")
    
# closes the output file
if WRITE_TO_FILE:
    out_file.close()
