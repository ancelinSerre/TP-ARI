"""
 +--------------------------------------------------------------+
 | File    : Search.py                                          |
 | Authors : Baptiste Bouvier and Ancelin Serre                 |
 | Year    : 2019                                               |
 | Polytech Grenoble - INFO4 - Accès et Recherche d'information |
 +--------------------------------------------------------------+
"""
# Standard imports
import os
from operator import itemgetter

# Project imports
from Request import Request

"""
Search class used to do
a research in a given corpus.
"""
class Search:

    """
    Search constructor
    :param:
        request, (Request object) preprocessed request
        nb_results, (int) number of results awaited by the user
        inverted_index, (dict) inverted index coming from the DataPreprocessor Object
        norms, (dict) documents norms coming from the DataPreprocessor Object
        file_path, (str) default file location for results
    """
    def __init__(self, request, nb_results, inverted_index, norms, utils):
        self.request        = request          # User request (Request object)
        self.nb_results     = nb_results       # Number of results awaited (int)
        self.inverted_index = inverted_index   # Inverted index (dict)
        self.norms          = norms            # Document norms (dict)
        self.file_path      = utils.rs_path    # Result files location
        self.res            = {}               # Raw result (dict)
        self.final_result   = []               # Result list for pretty print (list)

    """
    Function used to represent Search object
    """
    def __str__(self):
        display = ("+--------------------------------------------+\n"
                + "| " +str(len(self.final_result)) + " results found...\n"
                + "+--------------------------------------------+\n")
        rank = 1
        for elem in self.final_result[:self.nb_results]:
            name = elem["name"].replace(".sttr","")
            display += ("+--------------------------------------------+\n"
                      + "| " + str(rank) + " - [" + name + "] - [rel. " + self._get_relevance(elem["cosinus"]) + "] :" + "\n"
                      + "+--------------------------------------------+\n")
            result = ""
            with open(self.file_path+name) as f:
                nb_lines = 0
                for line in f:
                    result += "  "+line
                    nb_lines += 1
                    if nb_lines == 5:
                        break
                
            display += result
            rank += 1
        return display

    """
    Function used to execute the search in the corpus. 
    """
    def search(self):
        # Step 1 : Getting corresponding lines for each request term
        cor_lines = self._get_corresponding_lines()

        # Step 2 : Starting the search by computing cosinus for each document
        self._compute_document_cosinus(cor_lines)

        # Step 3 : Generating a list of results sorted on cosinus in desc order
        self._init_final_results()

        # Step 4 : Printing final results
        print(self)
        
    """
    Function used to get corresponding lines 
    for each request term in the inverted index
    :return:
        corresponding_lines, (dict)
    """
    def _get_corresponding_lines(self):
        # Getting corresponding lines for each request term
        # in the inverted index
        corresponding_lines = {}
        for word in self.request.vector_tfidf:
            if word in self.inverted_index:
                corresponding_lines[word] = self.inverted_index[word]["docs"]
        return corresponding_lines

    """
    Function used to compute document cosinus for each document
    by using the following formula for a document :
    cosinus_doc = sum(request_term_tfidf * document_term_tfidf) / request_norm * document_norm
    """
    def _compute_document_cosinus(self, corresponding_lines):
        # Intermediate step to compute results
        for word in corresponding_lines:
            # Getting TF.IDF for current word in request
            req_tfidf = self.request.vector_tfidf[word]
            for doc in corresponding_lines[word]:
                # Getting TF.IDF for current word in current document
                doc_tfidf = corresponding_lines[word][doc]
                # If we already saved a value for the current doc, 
                # we simply add the new one to it
                self.res[doc] = self.res.get(doc, 0) + (req_tfidf * doc_tfidf)

        # Dividing each value in the intermediate results by 
        # the multiplication of request norm and document norm
        for doc in self.res:
            self.res[doc] /= (self.request.norm * self.norms[doc])

    """
    Function used to initialize the list named final_results
    which corresponds to the search results sorted on cosinus value in desc order
    """
    def _init_final_results(self):
        # Placing final results in a list 
        # in order to be able to sort it in desc order
        self.final_result = []
        for doc in self.res:
            self.final_result.append({
                "name" : doc,
                "cosinus" : self.res[doc]
            })

        # Sorting final results on cosinus attribute in desc order
        self.final_result = sorted(self.final_result, key=itemgetter("cosinus"), reverse=True) 

    """
    Function used to estimate the relevance of a result
    using the cosinus value of this result
    :param:
        cosinus, (float) cosinus value computed during search execution
                it represents the relevance of a result between 0 and 1
    :return:
        relevance, (str) the result relevance represented as a string
                containing +, ++, +++ or ++++ from worst to best    
    """
    def _get_relevance(self, cosinus):
        relevance = "+"
        if 0.5 > cosinus >= 0.25:
            relevance = "++"
        elif 0.75 > cosinus >= 0.5:
            relevance = "+++"
        elif 1 >= cosinus >= 0.75:
            relevance = "++++"
        return relevance 

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        assert isinstance(value, Request)
        self._request = value

    @property
    def nb_results(self):
        return self._nb_results

    @nb_results.setter
    def nb_results(self, value):
        assert isinstance(value, int) 
        self._nb_results = value

    @property
    def inverted_index(self):
        return self._inverted_index

    @inverted_index.setter
    def inverted_index(self, value):
        assert isinstance(value, dict)
        self._inverted_index = value

    @property
    def norms(self):
        return self._norms

    @norms.setter
    def norms(self, value):
        assert isinstance(value, dict)
        self._norms = value

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        assert isinstance(value, str)
        try:
            if not os.listdir(value): raise FileNotFoundError()
        except FileNotFoundError:
            print("[Warning] No file found in the results file path given")
        except Exception as e:
            print(e)
            exit(1)
        finally:
            self._file_path = value
