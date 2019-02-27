"""
 +--------------------------------------------------------------+
 | File    : main.py                                          |
 | Authors : Baptiste Bouvier and Ancelin Serre                 |
 | Year    : 2019                                               |
 | Polytech Grenoble - INFO4 - Accès et Recherche d'information |
 +--------------------------------------------------------------+
"""
# Standard imports
import math
import nltk.stem.porter as porter
import argparse
import json
import copy

# Project imports
from Utils import Utils
from Request import Request 
from DataPreprocessor import DataPreprocessor
from Search import Search

"""
Function used to get user input, his request and the
number of results he wants
:return:
    request, (str) his request
    nb_res, (int) number of results awaited
"""
def get_user_input():
    # Getting user request
    request = input("[SearchEngine] >> Enter your request : ")
    if not request: exit(0)
    # Getting number of request awaited
    str_nb  = input("[SearchEngine] >> Enter the number of results you want : ")
    nb_res  = 0 
    # Casting it into an integer
    if str_nb and str_nb.isdigit():
        nb_res  = int(str_nb)
    else: exit(0)

    return (request, nb_res)

def save(dp):
    # Writing and saving salton representation and vocabulary and inverted index
    with open("inverted_index.json", "w") as v:
        v.write(json.dumps(dp.inv_index))

    # Removing redundant data before the save 
    # (tf is already visible in inverted index)
    salton_data = copy.deepcopy(dp.salton_rep)
    for doc in salton_data: del salton_data[doc]["vector_tf"]
    for doc in salton_data: salton_data[doc] = salton_data[doc]["vector_tfidf"]

    with open("salton_representation.json", "w") as v:
        v.write(json.dumps(salton_data))

    with open("vocabulary.json", "w") as v:
        v.write(json.dumps(dp.vocab))

    with open("norms.json", "w") as v:
        v.write(json.dumps(dp.norms))

if __name__ == "__main__":
    # Read user arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="json config file describing paths to use")
    parser.add_argument("--save",   help="save vocabulary, inverted index, document norms and more in a results folder", action="store_true")
    args = parser.parse_args()

    utils = None
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
            utils = Utils(**config)
    else:
        utils = Utils()
    


    dp = DataPreprocessor(utils)  # Instantiating a new DataPreprocessor
    dp.init_vocabulary()          # Initializing the vocabulary
    dp.init_salton()              # Initializing the salton vector representation
    dp.init_inverted_index()      # Initializing the inverted index
    dp.init_norms()               # Initializing norms list

    if args.save:
        save(dp)

    # Getting user request and number of request awaited
    (request, nb_res) = get_user_input()

    # Looping while request isn't empty
    while(True):

        # Instanitiating and preprocessing a new request
        request = Request(request, dp.vocab, utils)

        params = [request, nb_res, dp.inv_index, dp.norms, utils]
        s = Search(*params)
        s.search()

        # Getting user request and number of request awaited
        (request, nb_res) = get_user_input()