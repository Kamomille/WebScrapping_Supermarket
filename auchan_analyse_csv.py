
import pandas as pd

def moyenne_prix(csv, type):
    df = pd.read_csv(csv, sep=';')
    if (type != None) :df = df[df['type'] == type]
    df.prix = df.prix.str.replace(',', '.')
    df.prix = df.prix.astype(float)
    return df.prix.mean()
def nombre_produit(csv, type):
    df = pd.read_csv(csv, sep=';')
    if (type != None) :df = df[df['type'] == type]
    return len(df)

#Thiers 63300
#Billom 63160
print(moyenne_prix("auchan_csv/auchan_produits.csv", None))
print(moyenne_prix("auchan_csv/auchan_produits_lyon.csv", None))
print(moyenne_prix("auchan_csv/auchan_produits_billom 63160.csv", None))
print(nombre_produit("auchan_csv/auchan_produits.csv", None))
print(nombre_produit("auchan_csv/auchan_produits_lyon.csv", None))
print(nombre_produit("auchan_csv/auchan_produits_billom 63160.csv", None))


df1 = pd.read_csv("auchan_csv/auchan_produits.csv", sep=';')
df2 = pd.read_csv("auchan_csv/auchan_produits_lyon.csv", sep=';')
df3 = pd.read_csv("auchan_csv/auchan_produits_billom 63160.csv", sep=';')

liste_produit = list(df1.nom)







