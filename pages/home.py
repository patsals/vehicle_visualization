import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.Div('This is our Home page content.'),
])