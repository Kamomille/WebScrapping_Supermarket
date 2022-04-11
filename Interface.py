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
import auchan_search

Adresse_Auchan = pd.read_csv('Adresses_auchan.csv')
Auchan = Adresse_Auchan['Adresse']
Auchan = Auchan.values.tolist()

df_Produit_Auchan = auchan_search.create_csv_merge()
Produit = list(df_Produit_Auchan.index.get_level_values('nom'))

# Load data
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # initialisation du dash app

SIDEBAR_STYLE = {
    "position": "fixed", #ne bouge pas même quand on bouge la page
    "top": 0,
    "left": 0,
    "bottom": 0,
    #"transition": "all 0.5s",
    "width": "14rem",
    "padding": "4rem 1rem", #L'espace avec le haut puis l'espace avec la droite
    "background-color": "#f8f9fa",
    "background-position": "fixed"
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

navbar = dbc.NavbarSimple(children=[
        dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Carte", href="/"),
                dbc.DropdownMenuItem("Carte", href="/Carte"),
                dbc.DropdownMenuItem("Statistics", href="/Statistics"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Outils",
    brand_href="/",
    color="dark",
    dark=True,
    fluid=True
)

contentFilter = html.Div([
                    html.Div(children=[
                        html.H1('Where can I find the cheaper products ?'),
                        html.P('Enter the details to generate infographics')
                    ],
                        style={
                            'color': 'white',
                            'height': '5rem',
                            'text-align': "center",
                            "margin-left": "5rem",
                            "background-color": "black"
                        }
                    ),
                    html.Div([
                        dcc.Dropdown(Produit, id='dropdown', placeholder="Produit",
                             style={"width": "30rem",
                                    })],
                        style={"margin-top": "5rem",
                                "margin-left": "5rem",
                               'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

                    html.Div([
                        dcc.Dropdown(Auchan, id="dropdown2", placeholder="Localisation",
                              style={"width": "15rem",
                                     })],
                        style={"margin-left": "5rem",
                               "margin-top": "1rem",
                               'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

                    html.Div([
                        html.Button('Submit', id='submit-val', n_clicks=0,
                                style={
                                    "width": "5rem",
                                })],
                        style={"margin-left": "5rem",
                               "margin-top": "5rem",
                               'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

                    html.Div(id='container-button-basic',
                             children='Enter a value and press submit',
                             style={
                                 "margin-left": "6rem",
                                 "margin-top": "0rem",
                                 "margin-down": "50rem"
                             })
])

@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('dropdown', 'value'),
    State('dropdown2', 'value')
)
def Button_Submit(n_clicks, valueProd, valueLoc):

    return html.Div(['You choose "{}" and "{} '.format(
        valueProd,
        valueLoc
    )], style={'color': 'white'})

contentCard = html.Div([
                    html.Iframe(id='map', srcDoc=open('carte.html', 'r').read(), width='80%', height='600vh',
                                   )],
                        style = {
                            "margin-left": "5rem",
                            "textAlign": "center"}
                        )

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
    html.Div(children=[dcc.Graph(id='pie_chart_1',
                                 style={'textAlign': 'center', 'width': '40%', 'display': 'inline-block','margin-right':'1%'}),
                       dcc.Graph(id='pie_chart_2',
                                 style={'textAlign': 'center', 'width': '40%', 'display': 'inline-block','margin-right':'1%'}),
                       dcc.RadioItems(id='radio_button',
                                      options=[{'label': 'Ile-de-France VS the rest of France', 'value': 'choix_1'},
                                               {'label': 'The whole of France', 'value': 'choix_2'},
                                               {'label': 'By department', 'value': 'choix_3'},
                                               {'label': 'By region', 'value': 'choix_4'}],
                                      style={"margin-top": "3%",'color': 'black','width': '18%', 'display': 'inline-block','background-color': 'white'},
                                      value='choix_1'),
                       dcc.Graph(figure = auchan.population_VS_nbProduit_chart(), style={"margin-top": "50px"}),
                       dcc.Graph(figure = auchan.variance_chart(df), style={"margin-top": "50px"}),
                       ],
             style={"margin-left": "8rem", "margin-right": "2rem","margin-top": "5rem"}
)
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
    if (radio_button == 'choix_3'):
        DF_1 = auchan.nombre_de_produit_pas_cher_par_dep(df, 'minimum',list_name_csv_clean)
        DF_2 = auchan.nombre_de_produit_pas_cher_par_dep(df, 'maximum',list_name_csv_clean)
    if (radio_button == 'choix_4'):
        DF_1 = auchan.nombre_de_produit_pas_cher_par_region(df, 'minimum',list_name_csv_clean)
        DF_2 = auchan.nombre_de_produit_pas_cher_par_region(df, 'maximum',list_name_csv_clean)

    pie_chart_1 = px.pie(DF_1,
                            values='nb_prix',
                            names='localisation',
                            title='Percentage of number of CHEAPEST products')
    if (radio_button == 'choix_1'): pie_chart_1.update_traces(marker=dict(colors=['pink', 'orange']))

    pie_chart_2 = px.pie(DF_2,
                    values='nb_prix',
                    names='localisation',
                    title='Percentage of the number of MOST EXPENSIVE products')
    if (radio_button == 'choix_1'): pie_chart_2.update_traces(marker=dict(colors=['pink', 'orange']))

    return pie_chart_1, pie_chart_2
# ======================================================================================================================
#                               Layout slidebar
# ======================================================================================================================


app.layout = html.Div([
        dcc.Location(id="url"),
        sidebar,
        navbar,
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
        return [contentStatistics]
    else:
        return [html.H1("unfortunetly, we don't have anything yet")]


if __name__ == '__main__':
    app.run_server(debug=True)