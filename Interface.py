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

contentStatistics = html.Div([
    #Pour Camille - Mets tes graphiques ici, dis moi si tu as besoin de plus d'onglet faut juste ajouter
    #Une fois le "contentStatistics" remplis, descends dans le call back et change le return
])

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
        return [html.H1("unfortunetly, we don't have anything yet")] # Pour Camille - Juste ici !
    else:
        return [html.H1("unfortunetly, we don't have anything yet")]


if __name__ == '__main__':
    app.run_server(debug=True)