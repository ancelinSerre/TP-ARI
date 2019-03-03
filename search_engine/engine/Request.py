"""
 +--------------------------------------------------------------+
 | File    : Request.py                                         |
 | Authors : Baptiste Bouvier and Ancelin Serre                 |
 | Year    : 2019                                               |
 | Polytech Grenoble - INFO4 - Accès et Recherche d'information |
 +--------------------------------------------------------------+
"""
# Standard imports
import math
from nltk.tokenize import RegexpTokenizer

class Request():
    """
    Class Request used to preprocess
    the request given by the user before 
    to use it for a research.
    """
    def __init__(self, value, vocabulary, utils):
        """
        Request constructor
        :param: 
            value : str, the request content
            vocabulary : dict containing words and their df and idf
        """
        super().__init__()
        self.utils        = utils      # utils object used to get some files and directories path
        self.raw_request  = value
        self.request      = value      # request is a list of words
        self.vocabulary   = vocabulary # dict of words
        self.vector_tf    = {}         # vector is a dict of term frequency for this request
        self.vector_tfidf = {}         # vector is a dict of tfidf for this request
        self.norm         = 0          # request norm

        self._init_vector_tf()
        self._init_vector_tfidf()
        self._init_norm()

    def __str__(self):
        " Used to print the object state "
        return ("<class 'Request'>\n"
            + "- Raw request   : " + self.raw_request       + "\n"
            + "- Request       : " + str(self.request)      + "\n"
            + "- TF vector     : " + str(self.vector_tf)    + "\n"
            + "- TF.IDF vector : " + str(self.vector_tfidf) + "\n"
            + "- Norm          : " + str(self.norm))

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        pattern = r'[A-Za-z]\w{1,}'
        tokenizer = RegexpTokenizer(pattern)
        # Lowering every word and tokenizing it
        # in order to get a list
        reqst = tokenizer.tokenize(value.lower())
        # Applying porter truncature for each word which are not in anti dictionary
        reqst = [self.utils.get_root(req) for req in reqst if req not in self.utils.common_words]
        self._request = reqst
        
    def _init_vector_tf(self):
        " Used to initialize the vector of term frequency "
        for word in self.request:
            # Computing TF only consists in adding 1 
            # to the TF of the word every time we meet it
            self.vector_tf[word] = self.vector_tf.get(word, 0) + 1

    def _init_vector_tfidf(self):
        " Used to initialize the vector of TF.IDF weights "
        for word in self.vector_tf:
            # Verifying if the word exists in the vocabulary
            word_vocab = self.vocabulary.get(word, None)
            # Getting its Inverse Document Frequency
            word_idf   = word_vocab["idf"] if word_vocab else 0
            # Computing multiplication between TF and IDF
            self.vector_tfidf[word] = self.vector_tf[word] * word_idf

    def _init_norm(self):
        " Used to initialize the request norm "
        # Applying the following formula : sqrt(sum(wi**2))
        self.norm = math.sqrt(sum([self.vector_tfidf[word]**2 for word in self.vector_tfidf]))
