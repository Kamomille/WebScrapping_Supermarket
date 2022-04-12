import pandas as pd
from nltk.tokenize import word_tokenize
import string
import unidecode
import auchan_analyse_csv
from auchan_fonction_graph import create_list_df, get_list_csv_file


def tokenization_all_products(df):
    #df['nom_tokenizer'] = df.index.get_level_values('nom')
    df['nom_tokenizer'] = df['nom'].apply(lambda x: tokenization_one_product(x))
    return df

def tokenization_one_product(x):
    stop_words = ['à','avec' ,'au' ,'aux' ,'d' ,'pour' ,'on' ,'pas' ,'dans' ,'de' ,'des','un' ,'une' ,'du' ,'et' ,'en' ,
                  'est' ,'le' ,'la' ,'les','l','n','s' ,'a', 'q' ,'qu' ,'j' ,'t', 's','peu' ,'sans']
    new_word =""
    # -- on enlève la ponctuation --
    punct = string.punctuation
    try :
        for c in punct: x = x.replace(c, "")
    except:
        None
    # -- token --
    words = word_tokenize(x)
    for word in words:
        if word not in stop_words and not word.isdigit():
            if (word[-1] == "s" or word[-1] == "x"): word = word[:-1]  # met au singulier
            word = unidecode.unidecode(word) # enlève les accents
            new_word += word.lower() + " "
    new_word = new_word[:-1]  # enlève l'espace final
    return new_word


def filter(df, list_word_search):
    for i in range(len(list_word_search)):
        df = df[df['nom_tokenizer'].notnull()].copy()
        df['nom_tokenizer_contain'] = df['nom_tokenizer'].str.contains(list_word_search[i])
        df = df[df['nom_tokenizer_contain'] == True]
    return df #.loc[:, pd.IndexSlice[:, ['prix']]]


def filter_result(df, mot_demander):
    df_produits = tokenization_all_products(df)
    word_search = tokenization_one_product(mot_demander)
    df_filter = filter(df_produits,word_search.split(' '))
    return df_filter


# ---- inutile ----

def create_csv_merge():
    list_df, list_name_csv = create_list_df()
    list_concat_df =[]
    for i in range (len(list_df)):
        list_df[i] = list_df[i].drop_duplicates(subset= ["nom", "poids"])
        list_concat_df.append(list_df[i].set_index(["categorie","type","nom", "poids"]))
    df = pd.concat(list_concat_df,sort=False, axis=1, keys=list_name_csv)
    df.to_csv("auchan_csv/produits_merge.csv", sep=';')
    return df

"""
import auchan_fonction_graph as auchan

df_merge = auchan.create_csv_merge(True)
df, list_name_csv_clean = auchan.cleaning_data(df_merge)
df = df.reset_index()

print(filter_result(df))
"""
