from settings import *





# Variables for the output file, writing function, and tag array
OUT_FILE = open(FILE_OUT, "w")
WRITE = OUT_FILE.write if WRITE_TO_FILE else print
TAGS = [1] * PATTERN_COUNT





'''
General function for recording patterns

'case' is a selector for the pattern form that it fits
'outs' is a list of the noun phrases in text form that were extracted
'p1s' is a list of first words in the patterns that match
'p2s' is an optional list of second words in the patterns that match
'active' is for a couple of cases that combine active and passive voice

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
    # iterates through every combination of inputs
    for out in outs:
        for p1 in p1s:
            for p2 in p2s:
                # creates a tag number to put on the end if it isn't
                #  a premod
                if 1 <= case <= PATTERN_COUNT:
                    tag = "_" + str(TAGS[case - 1])

                # matches the case and prints the pattern
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

                # increments the tag array if it wasn't a premod
                if 1 <= case <= PATTERN_COUNT:
                    TAGS[case - 1] += 1

                # adds a newline if it's writing to a file
                if WRITE_TO_FILE:
                    WRITE("\n")
