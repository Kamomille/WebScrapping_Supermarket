import pandas as pd
import os
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

def get_list_csv_file():
    list = []
    for path, subdirs, files in os.walk('casino_csv_final'):
        for name in files:
            name = name.replace('casino__', '')
            name = name.replace('.csv', '')
            list.append(name) #os.path.join(path, name)
    return list

def create_list_df():
    list_name_csv = get_list_csv_file()
    list_df=[]
    for i in range (len(list_name_csv)):
        df = pd.read_csv("casino_csv_final/casino__" + list_name_csv[i] + ".csv", sep=';')
        df = df.drop(['promo', 'prix_par_kg'], axis=1)
        df['prix'] = df['prix'].str.replace('€','')
        df['prix'] = df['prix'].str.replace(',','.')
        df['prix'] = df['prix'].astype(float)

        df['poids'] = df['poids'].astype(str)
        df['poids'] = df.apply(lambda row: row["poids"][:-1] if row["poids"][-1] == 'g' else row["poids"], axis=1)
        df['poids'] = df['poids'].str.replace('Dosettes Rigides ','nan')
        df['poids'] = df['poids'].str.replace('Capsules Plastique ','nan')
        df['poids'] = df['poids'].str.replace('X','x')

        df['nom'] = df['nom'].str.lower()
        df['nom_split'] = df.apply(lambda row: row["nom"].split(' - cat'), axis=1)
        df['nom'] = df.apply(lambda row: row["nom_split"][0], axis=1)
        df = df.drop(columns=["nom_split"])
        list_df.append(df)
    return list_df, list_name_csv


def create_csv_merge(multiindex):
    list_df, list_name_csv = create_list_df()
    list_concat_df =[]
    for i in range (len(list_df)):
        list_df[i] = list_df[i].drop_duplicates(subset= ["categorie","type","nom","poids"])
        list_concat_df.append(list_df[i].set_index(["categorie","type","nom","poids"]))
    df = pd.concat(list_concat_df,sort=False, axis=1, keys=list_name_csv)
    if (multiindex == False) : df.columns = [col[0] for col in df.columns]
    df.to_csv("casino_produits_merge.csv", sep=';')
    return df

def cleaning_data (df):
    list_name_csv = get_list_csv_file()
    list_name_csv_new = []
    # Retirer les magasins ayant plus de 60% des produits vides
    for i in range (len(list_name_csv)):
        name = list_name_csv[i]
        if (df[name].prix.isna().sum()  * 100.0 / len(df) > 90 ):
            df.drop((name,'prix'), axis=1, inplace=True)
        else : list_name_csv_new.append(name)

    # Retirer les produits où il manque des données
    index_with_nan = df.index[df.isnull().any(axis=1)]
    df.drop(index_with_nan, axis=0, inplace=True)

    # Enlève le niveau 1 (= la ligne contenant le mot prix)
    df = df.droplevel(level = 1, axis=1)

    return df, list_name_csv_new


# ======================================================================================================================
#                               Variance
# ======================================================================================================================
def variance_calcul (df):
    DF = df.copy()
    DF["variance"] = df.var(axis=1)
    DF["nom_poids"] = DF.apply(lambda row: row["nom"] if row["nom"] == 'nan' else row["nom"] + ' | ' + row["poids"], axis=1)
    DF = DF.sort_values(by=['variance'], ascending=False)
    return DF

def variance_chart(df):
    variance_bar_chart = px.bar(variance_calcul(df),
                                y='variance',
                                x='nom_poids',
                                color='type',
                                title='Variances of different products')

    variance_bar_chart.update_xaxes(showticklabels=False)
    return variance_bar_chart
