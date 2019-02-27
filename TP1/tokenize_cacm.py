import os
from nltk.tokenize import RegexpTokenizer
import re

"""
Entry point
"""
if __name__ == "__main__":

    pattern = r'[A-Za-z]\w{1,}'
    tokenizer = RegexpTokenizer(pattern)    

    # Folder where CACM-XX are stored
    folder_name = "C:\\Users\\Ancelin\\Documents\\Cours\\S8\\RechInf\\TP1\\results\\"
    # Folder where to store .flt files
    tokenized_folder_name = "C:\\Users\\Ancelin\\Documents\\Cours\\S8\\RechInf\\TP1\\tokenized\\"
    # Reading every file
    for filename in os.listdir(folder_name):
        with open(folder_name+filename, "r") as f:
            words = []
            # Tokenizing each line of the file f
            for line in f:
                words += tokenizer.tokenize(line)

            # Lower every words
            words = [w.lower() for w in words]
            # Storing the result into a new file .flt
            with open(tokenized_folder_name+filename+".flt", "w") as output:
                for word in words:
                    output.write(word+" ")
