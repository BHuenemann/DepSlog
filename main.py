import spacy
import os
from spacy import displacy
from pathlib import Path
from functions import *
from settings import *





def process_doc(doc):
    # increments through each token and calls the functions to check for
    #  patterns
    for sent in get_sents(doc):
        for token in sent:
            base_passive(token)
            base_active(token)
            base_inf(token)
            base_aux(token)
            base_nprep(token)
            #addon_conj(token)
            #addon_predadj(token)
            #base_premod(token)


            
'''
Increments through all input files and calls the pattern functions.
'''
with open(FILE_OUT, "w") as out_file:
    count = 0
    iterator = range(0, 1) if CONSOLE_INPUT else iter(sorted(os.listdir(FILE_IN_PATH)))
    for file_name in iterator:
        if not CONSOLE_INPUT:
            if FILE_TYPE == "" and "." in file_name:
                continue
            elif not file_name.endswith(FILE_TYPE):
                continue

            # opens the file to read and creates the document for the dependency
            #  parser
            file_to_open = Path(FILE_IN_PATH + file_name)
            with open(file_to_open, 'r') as in_file:
                text = in_file.read()
            doc = create_doc(text)
            process_doc(doc)
        else:
            text = input("Enter a sentence: ")
            doc = create_doc(text)

            for sent in get_sents(doc):
                for token in sent:
                    print("\n  " + get_text(token) + \
                          "\n\t" + get_dep(token) + " --- " + get_text(get_head(token)) + \
                          "\n\t" + get_pos(token))
            print("\n")

            process_doc(doc)

        count += 1
        if WRITE_TO_FILE and PRINT_PROGRESS and count % PROGRESS_INTERVAL == 0:
            print("Processing file: " + file_name)

        # closes the file
        if not CONSOLE_INPUT:
            in_file.close()

# TEMPORARY -- displays the dependencies for easy viewing with displacy
displacy.serve(doc, style="dep")
