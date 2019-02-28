#  Accès et recherche d'information
**Auteurs** : Baptiste Bouvier et Ancelin Serre\
**Date** : 28/02/2019\
*POLYTECH GRENOBLE - INFO4*

## Sommaire

-  <a href="#tp1">TP1 : Loi de Zipf</a>
-  <a href="#tp2">TP2 : Constitution de vocabulaire et représentation</a>
-  <a href="#tp3">TP3 : Recherche et évaluation</a>

## <span id="tp1">TP1 : Loi de Zipf</a> 
Dans cette première étape, l'essentiel du travail consistait à préparer les fichiers `cacm` en un corpus "*tokenizé*" afin de pouvoir, par la suite, dresser une courbe représentant la fréquence d'apparation des termes du vocabulaire selon leur rang. Cela illustrait ainsi la fameuse [Loi de Zipf](https://hmul8r6b.imag.fr/lib/exe/fetch.php?media=accesinfoi-ii.pdf).
<br>
<br>
Pour effectuer ces tâches, nous avions déjà à dispositions le script `split_cacm.py` présent dans le répertoire `search_engine/preparation/` nous permettant de découper le fichier `cacm.all` en **3204** fichiers distincts. Notre premier travail à donc été de *tokenizer* chacun de ces fichiers.
<br>
Cela s'est traduit par le script suivant :
```python
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
```  
On voit bien ici que pour chaque fichier `cacm`, on utilise la fonction `tokenize()` en provenance du package *Python* `nltk` permettant de *tokenizer* un document selon un certain modèle défini dans la variable `pattern` avec une **expression régulière** chargée d'isoler chaque **terme** (pas de nombres ou autres caractères spéciaux) d'un fichier ligne après ligne. \
Une fois cette étape intermédiaire réalisée, on a juste à réécrire les données *tokenizées* en ajoutant pour chaque document tout ses mots sur une ligne, tous séparés par un `espace`. 
<br>
Ces fichiers seront finalement stockés dans le répertoire `search_engine/resources/tokenized/` avec l'extension `.flt`
<br>
<br>
Ces étapes étant désormais réalisées, il nous est maintenant aisé de calculer le lambda de la Loi de Zipf et de dresser son graphique. On trouve ainsi dans le script `zipf.py` : 
```python
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
```
Dans ce code, on se préoccupe essentiellement de calculer le nombre d'occurrences de chaque mot du corpus. Cela nous permet de calculer leur probabilité d'apparition et in fine de calculer la valeur du lambda. Ainsi, on créée un dictionnaire dans lequel pour chaque terme on sauvegarde sa probabilité d'apparition **pratique** (celle que l'on observe) et **théorique** (calculée selon le rang du terme et la valeur du lambda)

## <span id="tp2">TP2 : Constitution de vocabulaire et représentation</a> 
TODO

## <span id="tp3">TP3 : Recherche et évaluation</a> 
TODO