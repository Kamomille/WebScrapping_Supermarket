import pandas as pd
from nltk.tokenize import word_tokenize
import string
import unidecode
import auchan_analyse_csv
from auchan_fonction_graph import create_list_df, get_list_csv_file


def tokenization_all_products():
    df['nom_tokenizer'] = df.index.get_level_values('nom')
    df['nom_tokenizer'] = df['nom_tokenizer'].apply(lambda x: tokenization_one_product(x))
    return df

def tokenization_one_product(x):
    stop_words = ['à','avec' ,'au' ,'aux' ,'d' ,'pour' ,'on' ,'pas' ,'dans' ,'de' ,'des','un' ,'une' ,'du' ,'et' ,'en' ,
                  'est' ,'le' ,'la' ,'les','l','n','s' ,'a', 'q' ,'qu' ,'j' ,'t', 's','peu' ,'sans']
    new_word =""
    # -- on enlève la ponstuation --
    punct = string.punctuation
    for c in punct: x = x.replace(c, " ")
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
    return df.loc[:, pd.IndexSlice[:, ['prix']]]


def create_csv_merge():
    list_df, list_name_csv = create_list_df()
    list_concat_df =[]
    for i in range (len(list_df)):
        list_df[i] = list_df[i].drop_duplicates(subset= ["categorie","type","nom","poids"])
        list_concat_df.append(list_df[i].set_index(["categorie","type","nom","poids"]))
    df = pd.concat(list_concat_df,sort=False, axis=1, keys=list_name_csv)
    df.columns = [col[0] for col in df.columns]
    df.to_csv("auchan_csv/produits_merge.csv", sep=';')
    return df


def create_list_df():
    list_name_csv = get_list_csv_file()
    list_df=[]
    for i in range (len(list_name_csv)):
        df = pd.read_csv("auchan_csv/auchan_produits_" + list_name_csv[i] + ".csv", sep=';')
        list_df.append(df)
    return list_df, list_name_csv

def create_csv_merge():
    list_df, list_name_csv = create_list_df()
    list_concat_df =[]
    for i in range (len(list_df)):
        list_df[i] = list_df[i].drop_duplicates(subset= ["nom", "poids"])
        list_concat_df.append(list_df[i].set_index(["categorie","type","nom", "poids"]))
    df = pd.concat(list_concat_df,sort=False, axis=1, keys=list_name_csv)
    df.to_csv("auchan_csv/produits_merge.csv", sep=';')
    return df

df = create_csv_merge()

liste_produits = list(df.index.get_level_values('nom'))

df_produits = tokenization_all_products()

word_search = tokenization_one_product('Cookies noisette')

print("TABLEAU DES PRODUITS CORRESPONDANT A VOTRE RECHERCHE")
df_filter = filter(df_produits,word_search.split(' '))
print(df_filter)

"""
name_multiindex_columns = df.columns.get_level_values(0).unique()
name_multiindex_columns = name_multiindex_columns[:-1]
print(name_multiindex_columns)
for index, row in df_filter.iterrows():
    print("----- ",index[2], " -----")
    for i in range (len(name_multiindex_columns)):
        print(name_multiindex_columns[i], row[i])

"""

