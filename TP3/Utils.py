"""
 +--------------------------------------------------------------+
 | File    : Preprocessor.py                                    |
 | Authors : Baptiste Bouvier and Ancelin Serre                 |
 | Year    : 2019                                               |
 | Polytech Grenoble - INFO4 - Accès et Recherche d'information |
 +--------------------------------------------------------------+
"""
# Standard imports
import nltk.stem.porter as porter

"""
Class utils used to store paths used all along the program
"""
class Utils:

    # Default value for common words file
    DEFAULT_CD = "C:\\Users\\Ancelin\\Documents\\Cours\\S8\\RechInf\\TP1\\cacm\\common_words"
    # Default value for tokenized files directory
    DEFAULT_TD = "C:\\Users\\Ancelin\\Documents\\Cours\\S8\\RechInf\\TP1\\tokenized\\"
    # Default value for filtered word directory
    DEFAULT_FD = "C:\\Users\\Ancelin\\Documents\\Cours\\S8\\RechInf\\TP2\\stop_words_filtered\\"
    # Default Result File location
    FILE_PATH  = "C:\\Users\\Ancelin\\Documents\\Cours\\S8\\RechInf\\TP1\\results\\"

    """
    Utils constructor
    """
    def __init__(self, common_words=DEFAULT_CD, tokenized_files=DEFAULT_TD, 
        filtered_files=DEFAULT_FD, result_files=FILE_PATH):
        self.cw_path = common_words
        self.tk_path = tokenized_files
        self.ft_path = filtered_files
        self.rs_path = result_files
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