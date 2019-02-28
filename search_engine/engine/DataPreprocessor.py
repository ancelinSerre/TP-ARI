"""
 +--------------------------------------------------------------+
 | File    : DataPreprocessor.py                                |
 | Authors : Baptiste Bouvier and Ancelin Serre                 |
 | Year    : 2019                                               |
 | Polytech Grenoble - INFO4 - Accès et Recherche d'information |
 +--------------------------------------------------------------+
"""
# Standard imports
import os
import math

"""
Class DataPreprocessor used all along this file
to generate a vocabulary, a salton vector representation and
an inverted index from a given corpus.
"""
class DataPreprocessor():

    """
    Constructor for class DataPreprocessor
    """
    def __init__(self, utils):
        self.utils       = utils 
        self.files       = [] # List of files stored in memory
        self.vocab       = {} # Corpus vocabulary
        self.salton_rep  = {} # Salton vector representation
        self.inv_index   = {} # Inverted index
        self.norms       = {} # Document vector norms dict
        self._init_files()    # Initializing files first (it might take a long time)

    """
    Function used to initialize files dictionnary.
    """
    def _init_files(self):
        # Making a new directory for filtered word
        self.utils.safe_mkdir(self.utils.ft_path)
        # First we need to generate new documents with filtered words
        if not os.listdir(self.utils.ft_path):
            self._stop_list_filter()
        for filename in os.listdir(self.utils.ft_path):
            # We want to save the filename and its content
            current_file = {
                "name" : filename,
                "content" : []
            }
            with open(self.utils.ft_path+filename, "r") as f:
                for line in f:
                    for word in line.lower().split():
                        current_file["content"].append(word)
            self.files.append(current_file)

    """
    Function used to initialize the corpus vocabulary.
    """
    def init_vocabulary(self): 
        print("[DP] Initiating corpus vocabulary...")
        for document in self.files:
            for word in document["content"]:
                if word not in self.vocab:
                    self.vocab[word] = {   # We want fields to compute document frequency
                        "df" : 0,          # and inverse document frequency  
                        "idf": 0
                    }

        # compute Document Frequency DF for each word of the vocabulary
        self._compute_df()
        # now that we have computed DF for each terms, 
        # we can compute IDF using the following formula : idf_i = ln(N/df_i) 
        self._compute_idf()
        print("[DP] OK")

    """
    Function used to initialize salton representation using tf*idf.
    """
    def init_salton(self):
        if not self.vocab:
            self.init_vocabulary()
        print("[DP] Initiating Salton vector representation...")        
        for current_file in self.files:
            document = {
                "vector_tfidf" : {},
                "vector_tf"  : {}
            }
            # Computing tf for each term
            for term in current_file["content"]:
                if term in document["vector_tfidf"]:
                    document["vector_tfidf"][term] += 1
                    document["vector_tf"][term]  += 1
                else:
                    document["vector_tfidf"][term] = 1
                    document["vector_tf"][term]  = 1

            # Computing tf * idf for each term
            for term in document["vector_tfidf"]:
                document["vector_tfidf"][term] *= self.vocab[term]["idf"]       
            
            # Adding the current vector to the salton representation
            self.salton_rep[current_file["name"]] = document
        
        print("[DP] OK")

    """
    Function used to generate the inverted index
    Inverted index represents each word present in the corpus
    with its df and its tf for each file it is in.
    It doesn't compute anything, it just collects and regroups data.
    """
    def init_inverted_index(self):
        if not self.salton_rep:
            self.init_salton()
        print("[DP] Initiating Inverted index...")        
        for term in self.vocab:
            word = {
                "df" : self.vocab[term]["df"],
                "docs" : {}
            }
            for document in self.salton_rep:
                vector_tfidf = self.salton_rep[document]["vector_tfidf"]
                if term in vector_tfidf:
                    word["docs"][document] = vector_tfidf[term]
            
            self.inv_index[term] = word
        print("[DP] OK")        

    """
    Function used to compute vector norms of each document
    of the corpus using the following formula :
    ||vector|| = sqrt(sum(wi**2)) 
    with wi = idf_i in our case.
    """
    def init_norms(self):
        if not self.salton_rep:
            self.init_salton()
        print("[DP] Initiating Norms list...")        
        for doc in self.salton_rep:
            sum_square_wi = 0
            vector_tfidf = self.salton_rep[doc]["vector_tfidf"]
            for term in vector_tfidf:
                sum_square_wi += vector_tfidf[term]**2

            self.norms[doc] = math.sqrt(sum_square_wi) 
        print("[DP] OK")        

    """
    Function used to remove stop words / common words
    from each .flt tokenized files using a common words file.
    """
    def _stop_list_filter(self):
        # Folder where to store .flt files
        # Reading every file
        for filename in os.listdir(self.utils.tk_path):
            words = []
            with open(self.utils.tk_path+filename, "r") as f:
                for line in f:
                    curr_line = line.lower().split()
                    words += [self.utils.get_root(word) for word in curr_line if word not in self.utils.common_words]

            new_name = filename.replace(".flt", ".sttr")
            with open(self.utils.ft_path+new_name, "w") as f:
                for word in words:
                    f.write(word+" ")   

    """
    Function used to compute document frequency of each term in the vocabulary.
    """
    def _compute_df(self):
        for current_file in self.files:
            encountered = []
            for word in current_file["content"]:
                # Verify if we already encountered the word once in that file
                if word not in encountered:
                    self.vocab[word]["df"] += 1
                    encountered.append(word)

    """
    Function used to compute inverse document frequency of each term in the vocabulary.
    """
    def _compute_idf(self):
        N = len(self.files) # Number of document
        for term in self.vocab:
            self.vocab[term]["idf"] = math.log(N/self.vocab[term]["df"])