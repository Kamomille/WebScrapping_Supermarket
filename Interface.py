"""
https://medium.com/analytics-vidhya/brick-by-brick-build-a-multi-page-dashboard-dash-filters-dbec58d429d2
https://www.google.com/search?q=filter+folium+dash+python&rlz=1C1PRFI_enFR838FR838&oq=filter+folium+dash&aqs=chrome.1.69i57j33i160.11628j0j7&sourceid=chrome&ie=UTF-8
https://medium.com/generating-folium-maps-based-on-user-input-for-a/generating-folium-maps-based-on-user-input-for-a-dash-layout-16363da6ecd3
https://dash.plotly.com/dash-core-components/dropdown
"""


from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
#import auchan_search

Adresse_Auchan = pd.read_csv('Adresses_auchan.csv')
Auchan = Adresse_Auchan['Adresse']
Auchan = Auchan.values.tolist()

# Load data
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # initialisation du dash app

SIDEBAR_STYLE = {
    "position": "fixed", #ne bouge pas même quand on bouge la page
    "top": 0,
    "left": 0,
    "bottom": 0,
    #"transition": "all 0.5s",
    "width": "16rem",
    "padding": "2rem 1rem", #L'espace avec le haut puis l'espace avec la droite
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    #"transition": "margin-left .5s",
    "margin-left": "10rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    'background-image': 'url("/assets/Faire_ses_courses.jpg")',
    'background-repeat': 'no-repeat',
    'background-size': 'cover',
}

sidebar = html.Div([
    html.H2("Sidebar", className="display-4"),
    html.Hr(),
    #html.P("More", className="Lead"),
    dbc.Nav([
        dbc.NavLink("Filtre", href="/", id="page-1-link"),
        dbc.NavLink("Carte", href="/Carte", id="page-2-link"),
        dbc.NavLink("Statistics", href="/Statistics", id="page-3-link")],
        vertical=True, #On écrit les lien de haut en bas
        pills=True #La bar bleu qui apparait pour nous dire sur quelle page on est
    ),
], style=SIDEBAR_STYLE
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

contentFilter = html.Div([
                    html.Div(children=[
                        html.H1('Where can I find the cheaper products ?'),
                        html.P('Enter the details to generate infographics')
                    ],

                        style={
                            'color': 'white',
                            'width': '100%',
                            'height': '100px',
                            'text-align': "center",
                        }
                    ),
                    html.Div([
                        dcc.Dropdown(Auchan, id='dropdown', clearable=False,
                                     style={"width": "15rem",
                                            "margin-left": "4rem",
                                            "margin-top": "4rem",
                                            'display': 'inline-block',
                                            "margin-down": "50rem"
                                            }),

                        dcc.Input(id="Search_Bar", placeholder="produit", type='search',
                                    style={
                                        "margin-left": "6rem",
                                        "width": "20rem",
                                        "margin-top": "0rem",
                                        "margin-down": "50rem",
                                        'display': 'inline-block'
                                    })
                    ])])

contentCard = html.Div([
                        html.Iframe(id='map', srcDoc=open('carte.html', 'r').read(), width='80%', height='600vh',
                                    style={
                                        "margin-left": "6rem",
                                        "margin-right": "2rem",
                                        "margin-top": "0rem"})])

# ======================================================================================================================
#                               Partie Statistics
# ======================================================================================================================
import auchan_fonction_graph as auchan

df_merge = auchan.create_csv_merge(True)
df, list_name_csv_clean = auchan.cleaning_data(df_merge)
df = df.reset_index()

contentStatistics = html.Div([
    # ---- Texte en blanc ----
    html.Div(children=[html.H1('Statistics - Analyse Auchan\'s products'),
                       html.P('Number of scrapped Auchan stores :' + str(len(auchan.get_list_csv_file()))),
                       html.P('Number of Auchan stores after data cleaning :' + str(len(list_name_csv_clean)), )
                       ],
               style={'color': 'white','width': '100%','height': '100px','text-align': "center"}),

    # ---- Graphiques ----
    html.Div(children=[dcc.Graph(figure = auchan.population_VS_nbProduit_chart()),
                       html.Br(),
                       dcc.Graph(figure = auchan.variance_chart(df)),

                       dcc.RadioItems(id='radio_button',
                                      options=[{'label': 'Ile-de-France VS le reste de la France', 'value': 'choix_1'},
                                               {'label': 'Toute la France', 'value': 'choix_2'}],
                                      style={'color': 'white'},
                                      value='choix_1',),
                       dcc.Graph(id='pie_chart_1',
                                 style={'textAlign': 'center', 'width': '45%', 'display': 'inline-block','margin-right':'5%'}),
                       dcc.Graph(id='pie_chart_2',
                                 style={'textAlign': 'center', 'width': '45%', 'display': 'inline-block','margin-left':'5%'}),
                       ],
             style={"margin-left": "7rem", "margin-right": "2rem","margin-top": "5rem"}
)
    #Pour Camille - Mets tes graphiques ici, dis moi si tu as besoin de plus d'onglet faut juste ajouter
    #Une fois le "contentStatistics" remplis, descends dans le call back et change le return
])

@app.callback(Output('pie_chart_1', 'figure'),
              Output('pie_chart_2', 'figure'),
              Input('radio_button', 'value')
)
def update_pie_chart (radio_button):
    if (radio_button == 'choix_1'):
        DF_1 = auchan.ile_de_france_VS_reste(df, 'minimum',list_name_csv_clean)
        DF_2 = auchan.ile_de_france_VS_reste(df, 'maximum',list_name_csv_clean)
    if (radio_button == 'choix_2'):
        DF_1 = auchan.nombre_de_produit_pas_cher_par_ville(df, 'minimum',list_name_csv_clean)
        DF_2 = auchan.nombre_de_produit_pas_cher_par_ville(df, 'maximum',list_name_csv_clean)

    pie_chart_1 = px.pie(DF_1,
                            values='nb_prix',
                            names='localisation',
                            title='Percentage of number of CHEAPEST products in the store')
    if (radio_button == 'choix_1'): pie_chart_1.update_traces(marker=dict(colors=['pink', 'orange']))

    pie_chart_2 = px.pie(DF_2,
                    values='nb_prix',
                    names='localisation',
                    title='Percentage of the number of MOST EXPENSIVE products in the store')
    if (radio_button == 'choix_1'): pie_chart_2.update_traces(marker=dict(colors=['pink', 'orange']))

    return pie_chart_1, pie_chart_2
# ======================================================================================================================
#                               Layout slidebar
# ======================================================================================================================

app.layout = html.Div([
        dcc.Location(id="url"),
        sidebar,
        content
])

@app.callback(
    [Output("page-content", "children")],
    [Input("url", "pathname")], #On va prendre le pathname du url dans app.layout
)
def Content(pathname):
    if pathname == "/":
        return [contentFilter] #On retourne entre crochet,pour pouvoir envoyer au children de "content"
    elif pathname == "/Carte":
        return [contentCard]
    elif pathname == "/Statistics":
        #return [html.H1("unfortunetly, we don't have anything yet")] # Pour Camille - Juste ici !
        return [contentStatistics]
    else:
        return [html.H1("unfortunetly, we don't have anything yet")]


if __name__ == '__main__':
    app.run_server(debug=True)