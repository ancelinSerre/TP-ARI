"""
 +--------------------------------------------------------------+
 | File    : zipf.py                                            |
 | Authors : Baptiste Bouvier and Ancelin Serre                 |
 | Year    : 2019                                               |
 | Polytech Grenoble - INFO4 - Accès et Recherche d'information |
 +--------------------------------------------------------------+
"""
import os
import math
import matplotlib.pyplot as plt
from operator import itemgetter

def show_results(lambda_value, analysis):
    """
    :param:
        lambda_value, the lambda value (int)
        analysis,     
        a list of dictionnaries containing 
        some values like the word, its occurrence, 
        its theoretical occurrence and its probability
    """
    print("+----------------------------------------------------------------------+")
    print("| Zipf's Law : λ = " + str(lambda_value))
    print("| Rank\tWord\t\tOccurrence(s)\tTheoretical\tProbability (%)")
    print("+----------------------------------------------------------------------+")
    for i in range(0,10): 
        rank = i+1
        print("|  " 
            + str(rank) + "\t" 
            + analysis[i]["word"] + "\t\t" 
            + str(analysis[i]["occurrences"]) + "\t\t"
            + str(analysis[i]["theoretical"]) + "\t\t" 
            + str(analysis[i]["probability"])
        )

    print("+----------------------------------------------------------------------+")
    print("| Total number of word = " + str(total))
    print("+----------------------------------------------------------------------+")

def zipf_plot(analysis):
    """
    :param: analysis, 
        a list of dictionnaries containing 
        some values like the word, its occurrence, 
        its theoretical occurrence and its probability

    Plots the experimental and theoretical curves
    """
    # Plotting the result
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    axes = plt.gca()
    axes.set_xlim([0,1000])
    axes.set_ylim([0,1000])
    ranks = [rank for rank in range(0,len(analysis))]
    # Experimental in blue
    plt.plot(ranks, [data["occurrences"] for data in analysis], label="Practical")
    # Theoretical in orange
    plt.plot(ranks, [data["theoretical"] for data in analysis], label="Theoretical")
    plt.legend(loc='upper right')
    plt.show()

if __name__ == "__main__":
    """
    Entry point
    """
    # Folder where to store .flt files
    folder_name = "../resources/tokenized/"
    occurrences = {}
    words = []
    total = 0
    # Reading every file
    for filename in os.listdir(folder_name):
        with open(folder_name+filename, "r") as f:
            # Tokenizing each line of the file f
            for line in f:
                words += line.split()

    # Counting occurences of each word
    for word in words:
        occurrences[word] = occurrences.get(word, 0) + 1
        total += 1


    # Let's construct the analysis data structure
    analysis = []
    for word in occurrences :
        analysis.append({
            "word" : word,
            "occurrences" : occurrences[word],
            "probability" : round((occurrences[word] / total) * 100, 4)
        })

    # Sorting the values in desc order
    analysis     = sorted(analysis, key=itemgetter('probability'), reverse=True) 
    # Computing lambda value
    lambda_value = int(total / math.log(len(analysis)))
    # Adding theoretical occurrence for each word
    for i in range(0, len(analysis)):
        analysis[i]["theoretical"] = int(lambda_value/(i+1))


    """
    Fcthéorique ("de") = lambda / rang("de")
    lambda = M / ln(My)
    M  = nb total d'occurrences des mots
    My = nombre de mots différents
    """

    # Printing results
    show_results(lambda_value, analysis)

    # Plotting the result
    zipf_plot(analysis)