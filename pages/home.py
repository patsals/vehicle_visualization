import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/')

df = pd.read_csv('data/vehicle.csv', low_memory=False)


## COLORS
CATEGORY_COLORS = {
     'Regular Gasoline': px.colors.qualitative.D3[0],
     'Midgrade Gasoline': px.colors.qualitative.D3[1],
     'Premium Gasoline': px.colors.qualitative.D3[2],
     'Electricity': px.colors.qualitative.D3[3],
     'Diesel': px.colors.qualitative.D3[4]
}



# ################################################################################
                                                                                
#                                    PLOTTING                                    
                                                                                
# ################################################################################
def generate_ft_pie():
    most_recent_year = df['year'].max()
    temp = df[df['year'] == most_recent_year].groupby(['fuel_type_1']).count()
    temp = temp.reset_index().iloc[:, :2]
    temp.columns = ['fuel_type', 'count']

    fig = px.pie(temp,
                values='count',
                color='fuel_type',
                title=f'Number of Models Per Brand ({most_recent_year})',
                hover_name="fuel_type", 
    
                )   
    fig.update_layout(
            title=f'Fuel Type Distribution',
            font=dict(
                        size=14 
                    ),
            #plot_bgcolor='#111111',
            paper_bgcolor='#f0f0f0',
            #margin=dict(t=60),
            margin=dict(t=50, l=20, r=20, b=0), 
        )
    fig.update_traces(hole=0.4,
                  pull=[0.1, 0.1, 0.1, 0.1, 0.1],
                  marker=dict(colors=[CATEGORY_COLORS['Diesel'], 
                                      CATEGORY_COLORS['Electricity'],
                                      CATEGORY_COLORS['Midgrade Gasoline'], 
                                      CATEGORY_COLORS['Premium Gasoline'],   
                                      CATEGORY_COLORS['Regular Gasoline'], 
                                      ]
                            )
        )  # Specify custom color order

    return fig

def generate_mpg_kpi(type):
    most_recent_year = df['year'].max()
    temp = df[df['year'] == most_recent_year]

    current_mpg_ft1 = temp.groupby(['fuel_type_1'])[['unadjusted_city_mpg_ft1', 'unadjusted_highway_mpg_ft1']].mean().mean(axis=1)#.reset_index()
    current_mpg_ft1.columns = ['average mpg']

    temp = df[df['year'] == most_recent_year-1]
    previous_mpg_ft1 = temp.groupby(['fuel_type_1'])[['unadjusted_city_mpg_ft1', 'unadjusted_highway_mpg_ft1']].mean().mean(axis=1)#.reset_index()
    previous_mpg_ft1.columns = ['average mpg']
    current_mpg = round(current_mpg_ft1.loc[type], 2)
    difference_mpg = str(round(current_mpg_ft1.loc[type] - previous_mpg_ft1.loc[type], 2))
    style =  "bi bi-caret-up-fill me-2 text-success" if current_mpg_ft1.loc[type] > previous_mpg_ft1.loc[type] \
        else "bi bi-caret-down-fill me-2 text-danger"

    kpi_block = dbc.Card(
        dbc.CardBody(
            [
                html.Div(type + (' average mpge' if type == 'Electricity' else ' average mpg'),
                        #className='text-nowrap',
                        style={'font-size':'14px'}),
                      
                html.Hr(style={'margin':'auto', 'width':'75%'}),
                html.Div(current_mpg,
                         style={'font-size':'20px',
                                'font-weight':'bold',
                                'margin-top': '3px'}),
                html.Div(
                    [
                        html.I(difference_mpg, className=style),
                        'vs LY'
                    ]
                )
            ], className="border-color"
        ),
        className='text-center',
        style={'max-width': '200px',
               'border-style': 'none',
               'background-color':'#f0f0f0',
               'height':'120px'}
    )
    return kpi_block
    


def generate_savespend_bar():
    most_recent_year = df['year'].max()
    temp = df[df['year'] == most_recent_year]
    temp = temp.groupby(['fuel_type_1'])['save_or_spend_5_year'].mean().reset_index().iloc[:, :2]
    temp.columns = ['fuel type', 'amount saved']

    fig = px.bar(data_frame=temp, 
                x="fuel type", y="amount saved", 
                color="amount saved",
                color_continuous_scale=[[0, 'red'], [0.5, 'yellow'], [1, 'green']],
                hover_name="fuel type", 
                category_orders={'fuel type': ['Regular Gasoline', 'Midgrade Gasoline', 'Premium Gasoline', 'Diesel', 'Electricity']},
                )
    fig.update_layout(
            title=f'Average Amount Saved Over 5 years',
            font=dict(
                        size=14  # Set the font size to 14
                    ),
            #plot_bgcolor='#111111',
            paper_bgcolor='#f0f0f0',
            margin=dict(t=50, l=20, r=20, b=0)
        )
    fig.update_traces(opacity=0.7)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(showlegend=False)

    return fig



def generate_consumption_line():
    gallons_consumed = df.groupby(['fuel_type_1', 'year'])['annual_consumption_in_barrels_ft1'].mean().reset_index().iloc[:, :3]
    gallons_consumed.columns = ['fuel type', 'year', 'annual_consumption_in_barrels_ft1']
    gallons_consumed['annual consumed gallons'] = gallons_consumed['annual_consumption_in_barrels_ft1'] * 42

    fig = px.line(data_frame=gallons_consumed, 
                x="year", y="annual consumed gallons", 
                color="fuel type", 
                hover_name="fuel type", 
                category_orders={'fuel type': ['Regular Gasoline', 'Midgrade Gasoline', 'Premium Gasoline', 'Diesel', 'Electricity']},
                color_discrete_sequence=px.colors.qualitative.D3,
                )

    fig.update_layout(
            title=f'Average Annual Gallons Consumed',
            font=dict(
                        size=14  # Set the font size to 14
                    ),
            #plot_bgcolor='#111111',
            paper_bgcolor='#f0f0f0',
            margin=dict(t=50, l=20, r=20, b=0)
        )
   
    fig.update_layout(showlegend=False)

    return fig



@callback(
    Output(component_id='mpg-histogram', component_property='figure'),
    Input(component_id='type', component_property='value'),
)
def generate_mpg_hisogram(type):
    most_recent_year = df['year'].max()
    temp = df[df['year'] == most_recent_year]

    mpg_histograms = make_subplots(rows=5, cols=1)
    range_max = temp['highway_mpg_ft1'].max() + 20
    range_min = temp['highway_mpg_ft1'].min() - 20

    for i, type_color in enumerate(CATEGORY_COLORS.items()):
         ft_type, color = type_color
         mpg_histograms.add_trace(
              go.Histogram(x=temp[temp['fuel_type_1'] == ft_type][type],
                            nbinsx=50,
                            histnorm='percent',
                            marker_color=color,
                            name=ft_type
                            ), i+1, 1
         )
         
    mpg_histograms.update_xaxes(range=[range_min, range_max])

    mpg_histograms.update_yaxes(title_text='percentage', row=3, col=1)
    mpg_histograms.update_xaxes(title_text='mpg', row=5, col=1)
    mpg_histograms.update_layout(
            title=f"{type.split('_')[0].capitalize()} MPG(e) Distribution",
            font=dict(
                        size=14  # Set the font size to 14
                    ),
            #plot_bgcolor='#111111',
            paper_bgcolor='#f0f0f0',
            margin=dict(t=50, l=20, r=20, b=0)
        )
    mpg_histograms.update_layout(showlegend=False)

    return mpg_histograms



# ################################################################################
                                                                                
#                                  ADDITIONAL WIDGETS                                   
                                                                                
# ################################################################################
def generate_legend_widget(component):
    button = html.Button(className='bi bi-map', 
                         style= {'font-size':'24px', 'border': 'none', 'color':'rgba(0, 0, 0, 0.5)'}, 
                         id=component,
                         n_clicks=0
                         )
    
    popover = dbc.Popover(
                [
                    dbc.PopoverHeader("Legend"),
                    dbc.PopoverBody(
                        [html.Div(
                                [
                                    html.P(className='bi bi-square-fill', 
                                            style={'font-size':'14px', 
                                                'color':color,
                                                'margin':'0px'
                                                }
                                        ),
                                    html.P(type,
                                            style={'margin-bottom':'0px',
                                                   'margin-left':'4px'})
                                ], 
                                style={'display':'flex',
                                        'font-size':'14px',
                                        }
                            ) for type,color in CATEGORY_COLORS.items()]
                    ),
                ],
                target=component,
                placement='bottom',
                trigger="click",
                offset='50,5',
            )

    tooltip = dbc.Tooltip(
                "Legend",
                target=component,
                placement='top',
            )
    
    @callback(
        Output(component, 'className'),
        Input(component, 'n_clicks')
    )
    def change_fill(n_clicks):
            if n_clicks % 2 == 0:
                 return 'bi bi-map'
            else:
                return 'bi bi-map-fill'
    
    return [button, popover, tooltip]


def generate_info_widget(component, info_blurp):
    button = html.Button(className='bi bi-info-circle', 
                         style= {'font-size':'24px', 'border': 'none', 'color':'rgba(0, 0, 0, 0.5)'}, 
                         id=component,
                         n_clicks=0
                         )
    
    popover = dbc.Popover(
                [
                    dbc.PopoverHeader("Info"),
                    dbc.PopoverBody(
                        [html.Div(info_blurp)]
                    ),
                ],
                target=component,
                placement='bottom',
                trigger="click",
                offset='50,5',
            )

    tooltip = dbc.Tooltip(
                "Info",
                target=component,
                placement='top',
            )
    
    @callback(
        Output(component, 'className'),
        Input(component, 'n_clicks')
    )
    def change_fill(n_clicks):
            if n_clicks % 2 == 0:
                 return 'bi bi-info-circle'
            else:
                return 'bi bi-info-circle-fill'
    
    return [button, popover, tooltip]




# ################################################################################
                                                                                
#                                   MAIN LAYOUT                                   
                                                                                
# ################################################################################
layout = dbc.Container(
    children=[
        # FIRST ROW
        dbc.Row(
            children=[
                dbc.Col(generate_mpg_kpi(type), style={'margin': '10px'}) 
                for type in ['Regular Gasoline', 'Midgrade Gasoline', 'Premium Gasoline', 'Electricity', 'Diesel']
            ]
        ),

        # SECOND ROW
        dbc.Row([
            dbc.Col(
                html.Div(className='plot', 
                        children=[
                            dcc.Graph(figure=generate_ft_pie()),
                            html.Div(
                                [
                                    *generate_legend_widget('pie-legend'),
                                    *generate_info_widget('pie-info', 'AHHHHHH')
                                ],
                            )

                        ], #style={'height': '40vh'},
                        
                        #id='pie'
                ), lg=3, width={'size': 3},
            ),
            dbc.Col(
                html.Div(className='plot', 
                    children=[
                        dcc.RadioItems(
                            id='type',
                            options=[
                                {'label': 'Highway', 'value': 'highway_mpg_ft1'},
                                {'label': 'City', 'value': 'city_mpg_ft1'},
                            ],
                            value='highway_mpg_ft1',
                            labelStyle={'display': 'inline',
                                        'margin': '10px'}
                        ),
                        dcc.Graph(id='mpg-histogram'),
                        html.Div(
                                [
                                    *generate_legend_widget('histogram-legend'),
                                    *generate_info_widget('histogram-info', 'AHHHHHH')
                                ],
                            )
                    ], #style={'height': '40vh'}
                )#, width={'size': 6}
            ),
            
            ], align='center', 
        ),


        # THIRD ROW
        dbc.Row(
            [
                dbc.Col(
                    html.Div(className='plot', 
                        children=[
                            dcc.Graph(figure=generate_consumption_line()),
                            html.Div(
                                        [
                                            *generate_legend_widget('line-legend'),
                                            *generate_info_widget('line-info', 'AHHHHHH')
                                        ],
                                    )
                        ], #style={'height': '40vh'}
                    ), width={'size': 7}
                ),
                dbc.Col(
                    html.Div(className='plot', 
                        children=[
                            dcc.Graph(figure=generate_savespend_bar()),
                        ], #style={'height': '40vh'}
                    ), width={'size': 5}
                ),
            ], align='center'
        ),
    ], fluid=True
)