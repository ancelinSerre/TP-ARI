"""
 +--------------------------------------------------------------+
 | File    : tokenize_cacm.py                                   |
 | Authors : Baptiste Bouvier and Ancelin Serre                 |
 | Year    : 2019                                               |
 | Polytech Grenoble - INFO4 - Accès et Recherche d'information |
 +--------------------------------------------------------------+
"""
import os
from nltk.tokenize import RegexpTokenizer
import re

"""
Function used to make a directory, handling creation errors.
:param:
    name : (str) the directory name
"""
def safe_mkdir(name):
    # Creating a directory where to save generated files
    try:  
        os.mkdir(name)
    except OSError:  
        print("[Warning] Creation of the directory " + name + " failed")
    else:  
        print("[Info] Successfully created the directory " + name )
"""
Entry point
"""
if __name__ == "__main__":

    pattern = r'[A-Za-z]\w{1,}'
    tokenizer = RegexpTokenizer(pattern)    

    # Folder where CACM-XX are stored
    folder_name = "../resources/results/"
    # Folder where to store .flt files
    tokenized_folder_name = "../resources/tokenized/"
    safe_mkdir(tokenized_folder_name)

    # Reading every file
    for filename in os.listdir(folder_name):
        words = []
        with open(folder_name+filename, "r") as f:
            # Tokenizing each line of the file f
            for line in f:
                words += tokenizer.tokenize(line)

        # Lower every words
        words = [w.lower() for w in words]
        # Storing the result into a new file .flt
        with open(tokenized_folder_name+filename+".flt", "w") as output:
            for word in words:
                output.write(word+" ")

        print("File " + filename + " tokenized")
