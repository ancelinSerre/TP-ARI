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
import os
import argparse
import json
import copy
import nltk.stem.porter as porter

# Project imports
from Utils import Utils
from Request import Request 
from DataPreprocessor import DataPreprocessor
from Search import Search

def get_user_input():
    """
    Function used to get user input, his request and the
    number of results he wants
    :return:
        request, (str) his request
        nb_res, (int) number of results awaited
    """
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

def read_args():
    " Function used to read user arguments "
    # Read user arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="json config file describing paths to use")
    parser.add_argument("--save",   help="save vocabulary, inverted index, document norms and more in a results folder", action="store_true")
    return parser.parse_args()

def load_config(config_file):
    """
    Load specified .json config file in
    a ready-to-use dictionnary
    :param: 
        config_file : (str), config file name specified in args
    """
    config = {}
    with open(args.config) as f:
        config = json.load(f)
    return config

if __name__ == "__main__":
    # Reading user arguments
    args = read_args()
    # Instantiating a new Utils object 
    utils = Utils(**load_config(args.config)) if args.config else Utils()    

    dp = DataPreprocessor(utils)  # Instantiating a new DataPreprocessor
    dp.init_vocabulary()          # Initializing the vocabulary
    dp.init_salton()              # Initializing the salton vector representation
    dp.init_inverted_index()      # Initializing the inverted index
    dp.init_norms()               # Initializing norms list

    # Saving files if necessary before to start the search engine
    if args.save: utils.save(dp)

    # Getting user request and number of request awaited
    (request, nb_res) = get_user_input()

    # Looping while request isn't empty
    while(True):

        # Instanitiating and preprocessing a new request
        request = Request(request, dp.vocab, utils)

        # Processing the request
        params = [request, nb_res, dp.inv_index, dp.norms, utils]
        s = Search(*params)
        s.search()

        # Getting user request and number of request awaited
        (request, nb_res) = get_user_input()