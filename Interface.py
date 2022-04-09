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
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

navbar = dbc.NavbarSimple(children=[
        dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
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
    fluid=True,
)

#On ajoute un layout sur la page
sidebar = html.Div([
    html.H2("Sidebar", className="display-4"),
    html.Hr(),
    #html.P("More", className="Lead"),
    dbc.Nav([
        dbc.NavLink("Filtre", href="/", active="exact"),
        dbc.NavLink("Carte", href="/Carte", active="exact"),
        dbc.NavLink("Statistics", href="/Statistics", active="exact")],
        vertical=True,
        pills=True
    ),
],
    id ="sidebar",
    style=SIDEBAR_STYLE
)

content = html.Div([
                html.Div(children=[
                    html.H1('Where can I find the cheaper products ?'),
                    html.P('Enter the details to generate infographics')
                ],

                    style={
                        'color': 'black',
                        'width': '100%',
                        'height': '100px',
                        'text-align': "center"
                    }
                ),

                html.Div([
                    dcc.Input(
                        id="Search_Bar",
                        # placeholder="",
                        type='search'
                    ),
                    html.Div(id='Display-output')

                ],
                    style={
                        'width': '200rem',
                        'height': '200rem',
                        'text-align': "center"
                    }
                ),

                html.Div([
                    html.Iframe(id='map', srcDoc=open('carte.html', 'r').read(), width='80%', height='600vh')

                ],
                    id="page-content",
                    style=CONTENT_STYLE
                )

        ])

app.layout = html.Div([
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content

],
""" 
    style={
        'background-image': 'url("/assets/Faire_ses_courses.jpg")',
        'background-repeat': 'no-repeat',
        'width': '100%',
        'height': '100%',
        'background-size': 'cover',
        'background-position': 'center'
        }
"""
)
""" 
@app.callback(
    Output('dropdown', 'loc'),
    Input('dropdown', 'value')
)
def Localisation(selected_location):
    return f'You have selected {selected_location}'

@app.callback(
    Output('Search_Bar', 'Bar'),
    Input('Search_Bar', 'value')
)
def Result_Search(choix):
    return f'You have selected {Result}'
"""
@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)

def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick
""" 
@app.callback(
    Output('Display-output', 'children'),
    Input('Search_Bar', 'value')
)
def Result_Search(value):
    Result = auchan_search.Bar_De_Recherche(value)
    return f'You choose {Result}'
"""
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

