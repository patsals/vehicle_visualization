import dash
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP])

navbar = dbc.Nav(
    [
        dbc.NavLink(
            html.Div(page['name']),
            href=page['path'],
            active='exact',
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className='navbar-sticky',
    #style={'background-color':'white'}
)

app.layout = html.Div([
    dbc.Row([
        dbc.Col( 
            html.Div(
                [
                    html.H1('Fuel Economy Dashboard',
                            style={'margin-top': '30px',
                                'margin-bottom': '0px'}
                                ),
                    html.P('as of 2017',
                            style={'margin-top': '0px',
                                'margin-bottom': '30px'}
                                ),
                    html.Hr(),
                    navbar
                ],
                style={'padding':'10px'}
            ),
            width=2, 
            className='navbar',
            #style={'background-color':'red',}
        ),
        dbc.Col(
            #html.H1('hello', style={'background-color':'yellow'}),
            dash.page_container,
            width={'offset':2},
            #style={'background-color':'blue'}
        )
        ],
        style={'height': '100vh',}
    )
])



if __name__ == '__main__':
    app.run(debug=True)