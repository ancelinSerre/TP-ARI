"""
 +--------------------------------------------------------------+
 | File    : Preprocessor.py                                    |
 | Authors : Baptiste Bouvier and Ancelin Serre                 |
 | Year    : 2019                                               |
 | Polytech Grenoble - INFO4 - Accès et Recherche d'information |
 +--------------------------------------------------------------+
"""
# Standard imports
import os
import json
import copy
import nltk.stem.porter as porter

"""
Class utils used to store paths used all along the program
"""
class Utils:

    # Default value for common words file
    DEFAULT_CD = "../resources/cacm/common_words"
    # Default value for tokenized files directory
    DEFAULT_TD = "../resources/tokenized/"
    # Default value for filtered word directory
    DEFAULT_FD = "../resources/stop_words_filtered/"
    # Default Result File location
    FILE_PATH  = "../resources/results/"
    # Default Generated files location
    DEFAULT_GF = "../resources/generated_files/"

    """
    Utils constructor
    """
    def __init__(self, common_words=DEFAULT_CD, tokenized_files=DEFAULT_TD, 
        filtered_files=DEFAULT_FD, result_files=FILE_PATH, generated_files=DEFAULT_GF):
        self.cw_path = common_words
        self.tk_path = tokenized_files
        self.ft_path = filtered_files
        self.rs_path = result_files
        self.gf_path = generated_files
        self._common_words = []

    @property
    def common_words(self):
        # Initialize common_words if not already done
        if not self._common_words:
            self._init_common_words()
        return self._common_words

    """
    Function used to get a word's root
    based on Porter truncature.
    :param:
        word (string) the word to truncate
    :return:
        string, the word's root.
    """
    def get_root(self, word):
        stemmer = porter.PorterStemmer()
        return stemmer.stem(word)

    """
    Function used to extract all common words
    coming from the file located at self.cw_path
    """
    def _init_common_words(self): 
        with open(self.cw_path, "r") as f:
            self._common_words = [word.replace("\n","").lower() for word in f.readlines()]  

    """
    Function used to save files in a newly
    generated directory named ./generated_files
    """
    def save(self, dp):

        # Creating a directory where to save generated files
        try:  
            os.mkdir(self.gf_path)
        except OSError:  
            print("Creation of the directory " + self.gf_path + " failed")
        else:  
            print("Successfully created the directory " + self.gf_path )

        # Removing redundant data before the save 
        # (tf is already visible in inverted index)
        salton_data = copy.deepcopy(dp.salton_rep)
        for doc in salton_data: del salton_data[doc]["vector_tf"]
        for doc in salton_data: salton_data[doc] = salton_data[doc]["vector_tfidf"]

        # Indexing all the data to save
        results = {
            self.gf_path+"/inverted_index.json"        : dp.inv_index,
            self.gf_path+"/salton_representation.json" : salton_data,
            self.gf_path+"/vocabulary.json"            : dp.vocab,
            self.gf_path+"/norms.json"                 : dp.norms
        }

        # Writing results in results directory
        for data in results:
            with open(data, "w") as f:
                f.write(json.dumps(results[data]))