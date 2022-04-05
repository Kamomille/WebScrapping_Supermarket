"""
https://medium.com/analytics-vidhya/brick-by-brick-build-a-multi-page-dashboard-dash-filters-dbec58d429d2
https://www.google.com/search?q=filter+folium+dash+python&rlz=1C1PRFI_enFR838FR838&oq=filter+folium+dash&aqs=chrome.1.69i57j33i160.11628j0j7&sourceid=chrome&ie=UTF-8
https://medium.com/generating-folium-maps-based-on-user-input-for-a/generating-folium-maps-based-on-user-input-for-a-dash-layout-16363da6ecd3
https://dash.plotly.com/dash-core-components/dropdown
"""


from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import auchan_search

Adresse_Auchan = pd.read_csv('Adresses_auchan.csv')
Auchan = Adresse_Auchan['Adresse']
Auchan = Auchan.values.tolist()

# Load data
app = Dash(__name__)  # initialisation du dash app

#On ajoute un layout sur la page
app.layout = html.Div([
        html.Div(children = [
            html.H1('Where can I find the cheaper products ?'),
            html.P('Enter the details to generate infographics')
            ],

        style={
            'color': 'black',
            'width': '100%',
            'height': '100px',
            'text-align': "center"
            }),

        html.Div([
            dcc.Dropdown(Auchan, id='dropdown', clearable=False),
        ],
            style={
                'width': '20%',
                'height': '200px',
                'text-align': "center"
            }),

        html.Div([
            dcc.Input(
                id="Search_Bar",
                #placeholder="",
                type='search'
            ),
            html.Div(id='Display-output')

        ],
            style={
                'width': '20%',
                'height': '200px',
                'text-align': "center"
            }),

    html.Div([
        html.Iframe(id='map', srcDoc=open('carte.html', 'r').read(), width='80%', height='600vh')

    ], style={'padding': 50})

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
    Output('Display-output', 'children'),
    Input('Search_Bar', 'value')
)
def Result_Search(value):
    Result = auchan_search.Bar_De_Recherche(value)
    return f'You choose {Result}'


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

