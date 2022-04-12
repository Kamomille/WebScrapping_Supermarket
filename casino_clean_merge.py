import os
import pandas as pd

def get_list_csv_file():
    list = []
    for path, subdirs, files in os.walk('casino_csv'):
        for name in files:
            name = name.replace('casino_', '')
            name = name.replace('.csv', '')
            list.append(name) #os.path.join(path, name)
    return list

def create_list_df():
    list_name_csv = get_list_csv_file()
    list_df=[]
    for i in range (len(list_name_csv)):
        df = pd.read_csv("casino_csv/casino_" + list_name_csv[i].lower() + ".csv", sep=';')
        df = df.drop(['promo', 'prix_par_kg'], axis=1)
        df['prix'] = df['prix'].str.replace('€','')
        df['prix'] = df['prix'].str.replace(',','.')
        df['prix'] = df['prix'].astype(float)
        df['poids'] = df['poids'].astype(str)
        df['poids'] = df.apply(lambda row: row["poids"][:-1] if row["poids"][-1] == 'g' else row["poids"], axis=1)
        df['poids'] = df['poids'].str.replace('X','x')
        df['nom'] = df['nom'].str.lower()
        df['nom_split'] = df.apply(lambda row: row["nom"].split('cat'), axis=1)
        df['nom'] = df.apply(lambda row: row["nom_split"][0], axis=1)
        df.drop(columns=["nom_split"])
        list_df.append(df)
    return list_df, list_name_csv

def create_csv_merge():
    list_df, list_name_csv = create_list_df()
    list_concat_df =[]
    for i in range (len(list_df)):
        list_df[i] = list_df[i].drop_duplicates(subset= ["categorie","type","nom","poids"])
        list_concat_df.append(list_df[i].set_index(["categorie","type","nom","poids"]))
    df = pd.concat(list_concat_df,sort=False, axis=1, keys=list_name_csv)
    df.to_csv("casino_produits_merge.csv", sep=';')
    return df

print(get_list_csv_file())
create_list_df()
create_csv_merge()


