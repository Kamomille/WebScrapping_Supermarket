
#import auchan

import pandas as pd

df = pd.read_csv("auchan_produits.csv", sep=';')

df.prix = df.prix.str.replace(',', '.')
df.prix = df.prix.astype(float)

print(df.prix.mean())

