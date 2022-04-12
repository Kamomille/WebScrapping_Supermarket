import pandas as pd
import os
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')


def get_list_csv_file():
    list = []
    for path, subdirs, files in os.walk('auchan_csv'):
        for name in files:
            if (name != 'produits_merge.csv' and name != 'all_auchan_adresse.csv' and name != 'produits_cleaning.csv' and name != 'adresse_auchan_population.csv'):
                name = name.replace('auchan_produits_', '')
                name = name.replace('.csv', '')
                list.append(name) #os.path.join(path, name)
    return list

def create_list_df():
    list_name_csv = get_list_csv_file()
    list_df=[]
    for i in range (len(list_name_csv)):
        df = pd.read_csv("auchan_csv/auchan_produits_" + list_name_csv[i] + ".csv", sep=';')
        df = df.drop(['promo', 'prix_par_kg'], axis=1)
        df['prix'] = df['prix'].str.replace(',','.')
        df['prix'] = df['prix'].astype(float)
        df['poids'] = df['poids'].astype(str)
        df['poids'] = df.apply(lambda row: row["poids"][:-1] if row["poids"][-1] == 'g' else row["poids"], axis=1)
        df['poids'] = df['poids'].str.replace('X','x')
        df['nom'] = df['nom'].str.lower()
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
    df.to_csv("auchan_csv/produits_merge.csv", sep=';')
    return df

def cleaning_data (df):
    list_name_csv = get_list_csv_file()
    list_name_csv_new = []
    # Retirer les magasins ayant plus de 60% des produits vides
    for i in range (len(list_name_csv)):
        name = list_name_csv[i]
        if (df[name].prix.isna().sum()  * 100.0 / len(df) > 60 ):
            df.drop((name,'prix'), axis=1, inplace=True)
        else : list_name_csv_new.append(name)

    # Retirer les produits où il manque des données
    index_with_nan = df.index[df.isnull().any(axis=1)]
    df.drop(index_with_nan, axis=0, inplace=True)

    # Enlève le niveau 1 (= la ligne contenant le mot prix)
    df = df.droplevel(level = 1, axis=1)

    return df, list_name_csv_new

#def read_df_merge():
#    return pd.read_csv("auchan_csv/produits_merge.csv", sep=';', index_col=[0], header=[0,1])



def population_VS_nbProduit ():
    df_pop = pd.read_csv("auchan_csv/adresse_auchan_population.csv", sep=',')
    df_merge = create_csv_merge(True)
    list_name_csv = get_list_csv_file()
    list_nb_produit = []
    list_population = []
    for i in range (len(list_name_csv)):
        name = list_name_csv[i]
        list_nb_produit.append(len(df_merge) - df_merge[name].prix.isna().sum())
        df_pop_intermediaire =df_pop[df_pop['ville'] == name]
        list_population.append(df_pop_intermediaire['population'].values[0])
    DF = pd.DataFrame(list(zip(list_name_csv,list_nb_produit,list_population)), columns = ['localisation','nb_produit','population'])
    DF.sort_values(by=['population'], ascending=False)
    return DF

def population_VS_nbProduit_chart ():
    return px.scatter(population_VS_nbProduit(), x='population', y='nb_produit',hover_name='localisation',
                      labels={"y": "Number of products","x": "Number of inhabitants"},
                      title='Number of products available in each store according to the size of the city')


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

# ======================================================================================================================
#                               Pie chart
# ======================================================================================================================

def mettre_en_poucentage_en_fonction_prix_max (df, list_name_csv_clean):
    df["maximum"] = df.max(axis=1)
    for i in range (len(list_name_csv_clean)):
        name = list_name_csv_clean[i]
        df[name] = 100 * df[name] / df["maximum"]
    return df

def nombre_de_produit_pas_cher_par_ville (df, choix, list_name_csv_clean):
    DF = df.copy()
    list_nb = []
    if(choix == 'minimum'): DF["m"] = DF.min(axis=1, skipna=True)
    if (choix == 'maximum'): DF["m"] = DF.max(axis=1, skipna=True)
    for i in range (len(list_name_csv_clean)):
        name = list_name_csv_clean[i]
        DF[name] = DF.apply(lambda row: 1 if row["m"] == row[name] else 0, axis=1)
        list_nb.append(DF[list_name_csv_clean[i]].sum())
    intermediate_dictionary = {'localisation': list_name_csv_clean, 'nb_prix': list_nb}
    DF = pd.DataFrame(intermediate_dictionary)
    return DF

def nombre_de_produit_pas_cher_par_dep(df, choix, list_name_csv_clean):
    DF = nombre_de_produit_pas_cher_par_ville (df, choix, list_name_csv_clean)
    list_dep, prix = [], []

    DF['dep'] = DF.apply(lambda row: row["localisation"][:2], axis=1)
    list_dep = DF['dep'].unique()
    for i in range (len(list_dep)):
        DFF = DF[DF['dep'] == list_dep[i]]
        prix.append(DFF['nb_prix'].sum())
    DF = pd.DataFrame(list(zip(list_dep,prix)), columns = ['localisation','nb_prix'])
    return DF

def ile_de_france_VS_reste (df, choix, list_name_csv_clean):
    DF = nombre_de_produit_pas_cher_par_ville (df, choix, list_name_csv_clean)
    list_dep_iledefrance = ['77','78','75','91','92','93','94','95']
    DF['dep'] = DF.apply(lambda row: row["localisation"][:2], axis=1)
    DF_1 = DF[DF['dep'].isin(list_dep_iledefrance)]
    DF_2 = DF[~DF['dep'].isin(list_dep_iledefrance)]
    intermediate_dictionary = {'localisation': ['ile_de_france','autre'], 'nb_prix': [DF_1['nb_prix'].sum(), DF_2['nb_prix'].sum()]}
    DFF = pd.DataFrame(intermediate_dictionary)
    return DFF

def nombre_de_produit_pas_cher_par_region(df, choix, list_name_csv_clean):
    list_region = [['Auvergne-Rhône-Alpes','03','63','15','42','43','69','07','01','38','26','74','73'],
                    ['Bourgogne-Franche-Comté','89','58','21','71','70','39','25','90'],
                    ['Bretagne','29','22','56','35'],
                    ['Centre-Val de Loire','28','45','41','37','36','18'],
                    ['Corse','20'],
                    ['Grand Est','08','51','10','55','52','54','88','57','67','68'],
                    ['Hauts-de-France','62','59','80','02','60'],
                    ['Île-de-France','77','78','75','91','92','93','94','95'],
                    ['Normandie','50','14','76','27','61'],
                    ['Nouvelle-Aquitaine','79','86','87','23','19','16','17','24','33','47','40','64'],
                    ['Occitanie','46','12','48','30','34','81','82','32','31','65','09','11','66'],
                    ['Pays de la Loire','44','53','72','49','85'],
                    ['Provence-Alpes-Côte d\'Azur','84','13','83','04','05','06']]

    DF = nombre_de_produit_pas_cher_par_ville (df, choix, list_name_csv_clean)
    list_r, prix = [], []

    DF['dep'] = DF.apply(lambda row: row["localisation"][:2], axis=1)
    color = ['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A','#19D3F3','#FF6692','#B6E880','#FF97FF','#FECB52','#FECB52','#FECB52','#FECB52']

    for i in range (len(list_region)):
        DFF = DF[DF['dep'].isin(list_region[i])]
        list_r.append(list_region[i][0])
        prix.append(DFF['nb_prix'].sum())

    DF = pd.DataFrame(list(zip(list_r,prix, color)), columns = ['localisation','nb_prix','color'])
    return DF