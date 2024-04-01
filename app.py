import dash
from dash import Dash, html, dcc, callback, Input, Output



app = Dash(__name__, use_pages=True)



app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(
                f"{page['name']}",
                href=page["relative_path"],
                className="button-link"
            ),
        style={'display': 'inline-block'}
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])


if __name__ == '__main__':
    app.run(debug=True)