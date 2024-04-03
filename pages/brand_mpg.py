import dash
from dash import html, dcc, callback, Input, Output

import pandas as pd
import plotly.express as px

dash.register_page(__name__)

# https://www.kaggle.com/datasets/sahirmaharajj/fuel-economy
df = pd.read_csv('data/vehicle.csv', low_memory=False)
top_car_brands = [
    "Toyota",
    "Volkswagen",
    "Ford",
    "Honda",
    "Chevrolet"
]
df.loc[(df['unadjusted_city_mpg_ft2'] == 0), 'unadjusted_city_mpg_ft2'] = pd.NA
df.loc[(df['unadjusted_highway_mpg_ft2'] == 0), 'unadjusted_highway_mpg_ft2'] = pd.NA


layout = html.Div([
    #
    html.Div(className='two-columns', children=[
        # plot
        html.Div(className='left-column', children=[
            dcc.Tabs(id="fuel_type", value='1', children=[
                dcc.Tab(label='Fuel Type 1', value='1'),
                dcc.Tab(label='Fuel Type 2', value='2'),
            ]),
            dcc.Graph(id='plot', className='plot')
        ]),

        # make selections
        html.Div(className='right-column', children=[
            html.H3('Select Makes:'),
            dcc.Checklist(
                id='makes',
                options=df['make'].unique(),
                value=top_car_brands,
                style={'overflowY': 'scroll', 'height':'50vh'}
            )])
    ])

])




@callback(
    Output(component_id='plot', component_property='figure'),
    Input(component_id='makes', component_property='value'),
    Input(component_id='fuel_type', component_property='value'),

)
def update_make_mpg_plot(makes, fuel_type):
    temp = df[df['make'].isin(makes)]
    #temp = df[df['make'] == makes]
    mpg_ft1 = temp.groupby(['make', 'year'])[['unadjusted_city_mpg_ft1', 'unadjusted_highway_mpg_ft1']].mean().mean(axis=1).reset_index()
    mpg_ft2 = temp.groupby(['make', 'year'])[['unadjusted_city_mpg_ft2', 'unadjusted_highway_mpg_ft2']].mean().mean(axis=1).reset_index()
    mpg_ft1.columns = ['make', 'year', 'average_mpg_ft1']
    mpg_ft2.columns = ['make', 'year', 'average_mpg_ft2']

    if fuel_type == '1':
        fig = px.line(data_frame=mpg_ft1, 
                x="year", y="average_mpg_ft1", 
                    color="make", 
                    hover_name="make", 
                    )
    else:
        fig = px.line(data_frame=mpg_ft2, 
                x="year", y="average_mpg_ft2", 
                    color="make", 
                    hover_name="make", 
                    )
    return fig



def update_city_selected(input_value):
    return f'You selected: {input_value}'