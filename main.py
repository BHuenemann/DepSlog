from pathlib import Path
from functions import *
from settings import *





# opens the necessary output file to write to
if WRITE_TO_FILE:
    out_file = open(FILE_OUT, "w")

'''
Increments through all input files and calls the pattern functions
'''
for i in range(FILE_START, FILE_END + 1):
    # automatically adds a number to the end if there are multiple files
    #  and fills the number with 0s if that setting is active
    file_num = ""
    if MULT_FILES and FILL_DIGITS:
        file_num = str(i).zfill(DIGIT_COUNT)
    elif MULT_FILES:
        file_num = str(i)

    # opens the file to read and creates the document for the dependency
    #  parser
    file_to_open = Path(FILE_IN_PATH + FILE_IN + file_num)
    in_file = open(file_to_open, 'r')
    text = in_file.read()

    doc = create_doc(text)

    # increments through each token and calls the functions to check for
    #  patterns
    for token in doc:
        base_nsubj(token)
        base_nsubjpass(token)
        base_dobj(token)
        base_pobj(token)

    # closes the file and stops if there's only one input file
    in_file.close()

    if not MULT_FILES:
        break

# closes the output file
if WRITE_TO_FILE:
    out_file.close()
