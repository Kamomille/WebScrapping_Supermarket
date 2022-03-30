"""
https://www.google.com/search?q=filter+folium+dash+python&rlz=1C1PRFI_enFR838FR838&oq=filter+folium+dash&aqs=chrome.1.69i57j33i160.11628j0j7&sourceid=chrome&ie=UTF-8
https://medium.com/generating-folium-maps-based-on-user-input-for-a/generating-folium-maps-based-on-user-input-for-a-dash-layout-16363da6ecd3
"""


from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

Adresse_Auchan = pd.read_csv('Adresses_auchan.csv')
Auchan = Adresse_Auchan['Adresse']
Auchan = Auchan.values.tolist()

# Load data
app = Dash(__name__)  # initialisation du dash app

#On ajoute un layout sur la page
app.layout = html.Div([
        html.Div(children = [
            html.H1('Where can I find the cheaper product ?'),
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
            html.Div(id='dd-output-container')
        ],
            style={
                'width': '20%',
                'height': '200px',
                'text-align': "center"
            }),

        html.Div([
            dcc.Dropdown(['NYC', 'MTL', 'SF'], 'SF', id='dropdown2'),
            html.Div(id='dd-output-container2')
        ],
            style={
                'width': '20%',
                'height': '200px',
                'text-align': "center"
            }),

        html.Div([
            dcc.Input(
                id="input_{}".format(type),
                placeholder="input type {}".format(type),
                type='search'
            )],
            style={
                'width': '20%',
                'height': '200px',
                'text-align': "center"
            })

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

@app.callback(
    Output('dd-output-container', 'children'),
    Input('dropdown', 'value')
)
def update_output(value):
    print(value)
    return f'You have selected {value}'


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

""" 
app.layout = html.Div(children=[
    html.Iframe(id='map', srcDoc=open('carte.html', 'r').read(), width = '80%', height = '600vh')

], style = {'padding' : 50})"""