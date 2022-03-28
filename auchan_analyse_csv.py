import pandas as pd

def moyenne_prix(df, type):
    if (type != None) :df = df[df['type'] == type]
    df.prix = df.prix.str.replace(',', '.')
    df.prix = df.prix.astype(float)
    return df.prix.mean()
def nombre_produit(df, type):
    if (type != None) :df = df[df['type'] == type]
    return len(df)


def create_list_df(diplay):
    list_name_csv = ['Guilherand-Granges (Valence)',
                     'Auchan Piéton Lille Liberté',
                     'billom 63160',
                     'Auchan Piéton Périgueux Taillefer']
    list_df=[]
    for i in range (len(list_name_csv)):
        df = pd.read_csv("auchan_csv/auchan_produits_" + list_name_csv[i] + ".csv", sep=';')
        list_df.append(df)
        if (diplay == True):
            print("Moy prix " + list_name_csv[i] + " : ", moyenne_prix(df, None))
            print("Nb produit " + list_name_csv[i] + " : ", nombre_produit(df, None))
    return list_df, list_name_csv

def create_csv_merge():
    list_df, list_name_csv = create_list_df(False)
    list_concat_df =[]
    for i in range (len(list_df)):
        list_df[i] = list_df[i].drop_duplicates(subset= ["nom", "poids"])
        list_concat_df.append(list_df[i].set_index(["categorie","type","nom", "poids"]))
    df = pd.concat(list_concat_df,sort=False, axis=1, keys=list_name_csv)
    df.to_csv("auchan_csv/produits_merge.csv", sep=';')
    return df

df = create_csv_merge()


list_df, list_name_csv = create_list_df(False)

# Obtenir le prix de chaque lieu
print(df.loc[:, (list_name_csv, ['prix'])])

# Obtenir une liste des lignes avec des données manquantes
print(df.index[df.isnull().any(axis=1)])

# Obtenir les 3 lignes avec le plus grand nombre de données manquantes
print(df.isnull().sum(axis=1).nlargest(3))

# Obtenir le nom des produits présent dans tous les magasins (quels sont les produit de base?)
nb = len(df) - len(df.index[df.isnull().any(axis=1)])
print(nb)
print(df.isnull().sum(axis=1).nsmallest(nb))

# -- Commandes utiles --
#print(df.loc[:, (['Paris', 'Lyon'], ['prix'])])
#print(df.loc[:, pd.IndexSlice[:, ['prix', 'promo']]])
#print(df.Paris.prix[8])
#print(df.loc[:, ('Paris','prix')])
#print(df[('Paris','prix')])
#print(df.index.get_level_values('type'))




