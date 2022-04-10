import pandas as pd
import os
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
#import warnings
#warnings.filterwarnings('ignore')

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

def mettre_en_poucentage_en_fonction_prix_max (df, list_name_csv_clean):
    df["maximum"] = df.max(axis=1)
    for i in range (len(list_name_csv_clean)):
        name = list_name_csv_clean[i]
        df[name] = 100 * df[name] / df["maximum"]
    return df

def en_fonction_des_departement (df):
    df_departement = pd.DataFrame()
    df_departement['nom'] = df['nom']
    list_dep = []
    for j in range(0, 10):
        for i in range(1, 10):
            list_name_auchan = df.columns[3:]
            l = list(filter(lambda k: str(j)+str(i) in k[:2], list_name_auchan))
            if (len(l) > 0):
                DF = df.copy()
                df_departement[str(j)+str(i)] = DF[l].min(axis=1)
                list_dep.append(str(j)+str(i))
    return df_departement, list_dep

def nombre_de_produit_pas_cher_par_ville (df, choix,list_name_csv_clean):
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

def variance_calcul (df):
    DF = df.copy()
    DF["variance"] = df.var(axis=1)
    DF = DF.sort_values(by=['variance'], ascending=False)
    return DF

def ile_de_france_VS_reste (df, choix):
    DF = nombre_de_produit_pas_cher_par_ville (df, choix)
    list_dep_iledefrance = ['77','78','75','91','92','93','94','95']
    DF['dep'] = DF.apply(lambda row: row["localisation"][:2], axis=1)
    DF_1 = DF[DF['dep'].isin(list_dep_iledefrance)]
    DF_2 = DF[~DF['dep'].isin(list_dep_iledefrance)]
    intermediate_dictionary = {'localisation': ['ile_de_france','autre'], 'nb_prix': [DF_1['nb_prix'].sum(), DF_2['nb_prix'].sum()]}
    DFF = pd.DataFrame(intermediate_dictionary)
    return DFF

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
"""
# Application des fonctions
df = create_csv_merge(True)
df, list_name_csv_clean = cleaning_data(df)
df = df.reset_index()


# Enregister
df.to_csv("auchan_csv/produits_cleaning.csv", sep=';')



line_chart = px.scatter(population_VS_nbProduit(),
                     x='population',
                     y='nb_produit',
                        hover_name='localisation',
                     title='population_VS_nbProduit')

variance_bar_chart = px.bar(variance_calcul(df),
                            y='variance',
                            x='nom',
                            color='type',
                            title='Variances des différents produits')

variance_bar_chart.update_xaxes(showticklabels= False)


# --------------------------------- Interface dash ---------------------------------------------------------------------
app = Dash(__name__)
server=app.server

app.layout=html.Div(children =[
    html.H1(children="Analyse statistique", style={'textAlign': 'center'}),
    html.Hr(),
    html.P(children='Nombre de magasins Auchan scappé :'+ str(len(get_list_csv_file())), style={'textAlign': 'center'}),
    html.P(children='Nombre de magasins Auchan inclue dans l\'analyse :'+ str(len(list_name_csv_clean)), style={'textAlign': 'center'}),

    dcc.Graph(figure=line_chart ),

    dcc.RadioItems(
        id='radio_button_2',
        options=[{'label': 'Ile-de-France VS le reste de la France', 'value': 'choix_1'},
                 {'label': 'Toute la France', 'value': 'choix_2'}],
        value='choix_1',
    ),

    dcc.Graph(id='pie_chart_1',
              style={'textAlign': 'center', 'width': '45%','display': 'inline-block'},),

    dcc.Graph(id='pie_chart_2',
              style={'textAlign': 'center', 'width': '45%','display': 'inline-block'},),

    dcc.Graph(figure= variance_bar_chart),

])


@app.callback(Output('pie_chart_1', 'figure'),
              Output('pie_chart_2', 'figure'),
              Input('radio_button_2', 'value')
)

def update_pie_chart (radio_button_2):
    if (radio_button_2 == 'choix_1'):
        DF_1 = ile_de_france_VS_reste(df, 'minimum')
        DF_2 = ile_de_france_VS_reste(df, 'maximum')
    if (radio_button_2 == 'choix_2'):
        DF_1 = nombre_de_produit_pas_cher_par_ville(df, 'minimum')
        DF_2 = nombre_de_produit_pas_cher_par_ville(df, 'maximum')

    pie_chart_1 = px.pie(DF_1,
                            values='nb_prix',
                            names='localisation',
                            title='Pourcentage du nb de produits le MOINS cher dans le magasin')
    if (radio_button_2 == 'choix_1'): pie_chart_1.update_traces(marker=dict(colors=['blue', 'red']))

    pie_chart_2 = px.pie(DF_2,
                    values='nb_prix',
                    names='localisation',
                    title='Pourcentage du nb de produits le PLUS cher dans le magasin')
    if (radio_button_2 == 'choix_1'): pie_chart_2.update_traces(marker=dict(colors=['blue', 'red']))

    return pie_chart_1, pie_chart_2

if __name__ == '__main__':
    app.run_server() #debug=True

"""
"""

    dcc.RadioItems(
            id='radio_button',
            options=[
                #{'label': 'Tout', 'value': 'choix_1'},
                     {'label': 'Marque Auchan', 'value': 'choix_2'},
                     {'label': 'Marque Auchan BIO', 'value': 'choix_3'},
                     {'label': 'Toutes les marques sauf Auchan', 'value': 'choix_4'},
                     {'label': 'Toutes les légumes bio', 'value': 'choix_5'},
                     {'label': 'Tous le BIO', 'value': 'choix_6'},
                     {'label': 'Par département', 'value': 'choix_7'}],
            value='choix_5',
        ),
        dcc.Graph(id='scatter',
          style={'height': '800px'}),

@app.callback(Output('scatter', 'figure'),
              Input('radio_button', 'value')
)

def update_bar (radio_button):
    DF = mettre_en_poucentage_en_fonction_prix_max()
    list_name = list_name_csv_clean
    #if (radio_button == 'choix_1'): DF = DF.copy()
    if (radio_button == 'choix_2'): DF = DF[DF['nom'].str[:6] == 'AUCHAN']
    if (radio_button == 'choix_3'): DF = DF[DF['nom'].str[:10] == 'AUCHAN BIO']
    if (radio_button == 'choix_4'): DF = DF[DF['nom'].str[:6] != 'AUCHAN']
    if (radio_button == 'choix_5'): DF = DF[DF['type'] == 'Bio']
    if (radio_button == 'choix_6'): DF = DF[DF['nom'].str.contains('Bio') | DF['nom'].str.contains('bio') | DF['nom'].str.contains('BIO')]
    if (radio_button == 'choix_7'): DF, list_name = en_fonction_des_departement()

    x, y, z = [], [], []
    for i in range(len(list_name)):
        name = list_name[i]
        x += list(DF['nom'])
        y += list(DF[name])
        z += [name] * len(list(DF[name]))
    scatter = px.scatter(y=y, x=x, color=z,
                         labels={
                             "y": "Pourcentage",
                             "x": "Nom du produit",
                             "z": "Nom de la ville"
                         },
                         title="Répartition des prix d'Auchan en pourcentage par rapport au produit le plus cher" )
    scatter.update_xaxes(showticklabels= False)
    return scatter
"""



"""

def commandes_utiles(df):
    list_df, list_name_csv = create_list_df()
    print('-------------- le prix pour chaque lieu --------------')
    #print(df.loc[:, (list_name_csv, ['prix'])])

    print('-------------- Obtenir une liste des lignes avec des données manquantes --------------')
    print(df.index[df.isnull().any(axis=1)])

    print('-------------- Obtenir les 3 lignes avec le plus grand nombre de données manquantes --------------')
    print(df.isnull().sum(axis=1).nlargest(3))

    print('-------------- Obtenir le nom des produits présent dans tous les magasins (quels sont les produit de base?) --------------')
    nb = len(df) - len(df.index[df.isnull().any(axis=1)])
    print(nb)
    print(df.isnull().sum(axis=1).nsmallest(nb))

    print('-------------- Obtenir les magasins ayant + de 50% des produits --------------')
    column_with_nan = df.columns[df.isna().any()]
    for column in column_with_nan:
        if df[column].isna().sum() * 100.0 / len(df[column]) < 50:
            print(column)

    print('-------------- Obtenir les produits présent dans - de 50% des magasins --------------')
    for i in range (len(list_name_csv)):
        print(list_name_csv)
        print(df[i].isna().sum() * 100.0 / len(df) > 50)

    print('-------------- Obtenir les magasins ayant le + de promot --------------')


# -- Commandes utiles --
#print(df.loc[:, (['Paris', 'Lyon'], ['prix'])])
#print(df.loc[:, pd.IndexSlice[:, ['prix', 'promo']]])
#print(df.Paris.prix[8])
#print(df.loc[:, ('Paris','prix')])
#print(df[('Paris','prix')])
#print(df.index.get_level_values('type'))
#print(df.columns.get_loc('02500 Hirson'))


# ========================= BROUILLON ==================================================================================

def reparation_de_betise_bis():
    list_name_csv = ['27670 Le Bosc Roger En Roumois', '20167 Sarrola Carcopino', '30100 Ales', '31390 Carbonne',
            '31140 Launaguet', '31200 Toulouse']
    list_name_csv = get_list_csv_file()
    for i in range (len(list_name_csv)):
        df = pd.read_csv("auchan_csv/auchan_produits_" + list_name_csv[i] + ".csv", sep=';')
        try: del df["Unnamed: 0"]
        except:print('n')
        df.type = df.type.replace('Petit dej', 'Petit dej, boissons chaudes')
        df.to_csv("auchan_csv/auchan_produits_" + list_name_csv[i] + ".csv", sep=';',index=False)
#reparation_de_betise_bis()

def reparation_de_betise():
    df = pd.read_csv("auchan_csv/auchan_produits_31200 Toulouse.csv", sep=';')
    list_type = ['Bio', 'Fruit', 'Légumes', 'Prêt à consommer', 'Cafe', 'Petit dej', 'Biscuits, gateaux',
                 'Chocolat, confiseries', 'Dessert, sucre, farine']
    caractere_2 = "B"
    compt = 0
    for i in df.index:
        caractere_1 = df.loc[i, 'type']
        if (caractere_1 != caractere_2): compt += 1
        df.loc[i, 'type'] = list_type[compt]
        caractere_2 = caractere_1
    df.to_csv('auchan_csv/auchan_produits_31200 Toulouse.csv', sep=';')
"""
