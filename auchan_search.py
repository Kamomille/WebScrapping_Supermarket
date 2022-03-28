from nltk.tokenize import word_tokenize
import re
import string
import pandas as pd
import auchan_analyse_csv

df = auchan_analyse_csv.create_csv_merge()

liste_produits = list(df.index.get_level_values('nom'))


def tokenization_all_products():
    new_liste = []
    for i in range (len(liste_produits)):
        new_word = tokenization_one_product(liste_produits[i])
        new_liste.append(new_word)
    return new_liste

def tokenization_one_product(x):
    stop_words = ['à' ,'avec' ,'au' ,'aux' ,'d' ,'pour' ,'on' ,'pas' ,'dans' ,'de' ,'des',
                  'un' ,'une' ,'du' ,'et' ,'en' ,'est' ,'le' ,'la' ,'les' ,'n' ,'s' ,'a',
                  'q' ,'qu' ,'j' ,'t' ,'peu' ,'sans']
    new_word =""
    # -- on enlève la ponstuation --
    punct = string.punctuation
    for c in punct: x = x.replace(c, " ")
    # -- token --
    words = word_tokenize(x)
    for word in words:
        if word not in stop_words and not word.isdigit():
            if (word[-1] == "s" or word[-1] == "x"): word = word[:-1]  # met au singulier
            new_word += word.lower() + " "
    new_word = new_word[:-1]  # enlève espace de fin
    return new_word


def Filter(datalist, word_search):
    return [val for val in datalist
            if re.search(r'^' + str(word_search), val)]


def filter_n(datalist, list_word_search):
    for i in range(len(list_word_search)):
        datalist = list(filter(lambda k: list_word_search[i] in k, datalist))
    print(datalist)



liste_produits = tokenization_all_products()

word_search = tokenization_one_product('pomme de terre')

filter_n (liste_produits,word_search.split(' '))

