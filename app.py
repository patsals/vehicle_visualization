import dash
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

navbar = dbc.Nav(
    [
        dbc.NavLink(
            [html.Div(page['name'], className='ms-3')],
            href=page['path'],
            active='exact'
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className='bg-light navbar-sticky'
)

app.layout = html.Div([

    html.Div(className='navbar-columns', children=[
        html.Div(className='navbar-left-column', children=[
                html.H1('Fuel Economy Dashboard',
                        style={'margin-top': '30px',
                               'margin-bottom': '30px'}),
                html.Hr(),
                navbar
        ]),
        html.Div(dash.page_container, className='navbar-right-column')
    ])
])


if __name__ == '__main__':
    app.run(debug=True)