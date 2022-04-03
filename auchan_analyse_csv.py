import pandas as pd
import os
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px

def get_list_csv_file():
    list = []
    for path, subdirs, files in os.walk('auchan_csv'):
        for name in files:
            if (name != 'produits_merge.csv' and name != 'all_auchan_adresse.csv' and name != 'produits_cleaning.csv'):
                name = name.replace('auchan_produits_', '')
                name = name.replace('.csv', '')
                list.append(name) #os.path.join(path, name)
    return list

def create_list_df(display):
    list_name_csv = get_list_csv_file()
    list_df=[]
    for i in range (len(list_name_csv)):
        df = pd.read_csv("auchan_csv/auchan_produits_" + list_name_csv[i] + ".csv", sep=';')
        df = df.drop(['promo', 'prix_par_kg','poids'], axis=1)
        df['prix'] = df['prix'].str.replace(',','.')
        df['prix'] = df['prix'].astype(float)
        #df["poids"] = df.apply(lambda row: row["poids"][:-1] if row["poids"][-1] == 'g' else row["poids"], axis=1)
        list_df.append(df)
        if (display == True):
            print("Moy prix " + list_name_csv[i] + " : ", df.prix.mean())
            print("Nb produit " + list_name_csv[i] + " : ", len(df))
    return list_df, list_name_csv

def create_csv_merge(multiindex):
    list_df, list_name_csv = create_list_df(False)
    list_concat_df =[]
    for i in range (len(list_df)):
        list_df[i] = list_df[i].drop_duplicates(subset= ["categorie","type","nom"]) #subset= ["nom", "poids"]
        list_concat_df.append(list_df[i].set_index(["categorie","type","nom"])) #"poids"
    df = pd.concat(list_concat_df,sort=False, axis=1, keys=list_name_csv)
    if (multiindex == False) : df.columns = [col[0] for col in df.columns]
    df.to_csv("auchan_csv/produits_merge.csv", sep=';')
    return df

def cleaning_data (df):
    list_name_csv = get_list_csv_file()
    list_name_csv_new = []
    # Retirer les magasins ayant plus de 50% des produits vides
    for i in range (len(list_name_csv)):
        name = list_name_csv[i]
        if (df[name].prix.isna().sum()  * 100.0 / len(df) > 50 ):
            df.drop((name,'prix'), axis=1, inplace=True)
        else : list_name_csv_new.append(name)

    # Retirer les produits où il manque des données
    index_with_nan = df.index[df.isnull().any(axis=1)]
    df.drop(index_with_nan, axis=0, inplace=True)

    # Enlève le niveau 1 (= la ligne contenant le mot prix)
    df = df.droplevel(level = 1, axis=1)

    return df, list_name_csv_new


df = create_csv_merge(True)
df, list_name_csv_clean = cleaning_data(df)

df["maximum"] = df.max(axis=1)

for i in range (len(list_name_csv_clean)):
    name = list_name_csv_clean[i]
    df[name] = 100 * df[name] / df["maximum"]

df = df.reset_index()


#scatter.show()

# Enregister
df.to_csv("auchan_csv/produits_cleaning.csv", sep=';')



app = Dash(__name__)
server=app.server

app.layout=html.Div(children =[
    html.H1(children="Analyse statistique", style={'textAlign': 'center'}),
    html.Hr(),
    dcc.RadioItems(
        id='radio_button',
        options=[{'label': 'Tout', 'value': 'choix_1'},
                 {'label': 'Par marque', 'value': 'choix_2'},
                 {'label': 'Par catégorie', 'value': 'choix_3'},
                 {'label': 'Par département', 'value': 'choix_4'}],
        value='choix_1',
    ),
    dcc.Graph(id='scatter',
              style={'height': '800px'}),
])


@app.callback(Output('scatter', 'figure'),
              Input('radio_button', 'value')
)

def update_bar (radio_button):
    if (radio_button == 'choix_1'):
        x, y, z = [], [], []
        for i in range(len(list_name_csv_clean)):
            name = list_name_csv_clean[i]
            x += list(df['nom'])
            y += list(df[name])
            z += [name] * len(list(df[name]))
        scatter = px.scatter(y=y, x=x, color=z)

    scatter.update_xaxes(showticklabels= False)
    return scatter

if __name__ == '__main__':
    app.run_server(debug=True)







"""



def commandes_utiles(df):
    list_df, list_name_csv = create_list_df(False)
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


#commandes_utiles(df)
#create_list_df(True)
#df.prix.mean()


# -- Par département
#liste_nom_lieu = get_list_csv_file()
#for i in range (96):
#    df_prix_lieu = df.loc[:, ('Paris','prix')]




# -- Commandes utiles --
#print(df.loc[:, (['Paris', 'Lyon'], ['prix'])])
#print(df.loc[:, pd.IndexSlice[:, ['prix', 'promo']]])
#print(df.Paris.prix[8])
#print(df.loc[:, ('Paris','prix')])
#print(df[('Paris','prix')])
#print(df.index.get_level_values('type'))
#print(df.columns.get_loc('02500 Hirson'))

# -- A tester --
#df = df.filter(regex="Adj Close")




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
