import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.Div('This is our Archive page content.'),
])