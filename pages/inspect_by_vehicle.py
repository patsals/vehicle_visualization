import dash
from dash import html

dash.register_page(__name__)
popular_car_brands_us = [
    "Ford",
    "Chevrolet",
    "Toyota",
    "Honda",
    "Nissan",
    "Jeep",
    "RAM",
    "GMC",
    "Hyundai",
    "Subaru",
    "Kia",
    "Volkswagen",
    "Mercedes-Benz",
    "BMW",
    "Audi",
    "Lexus",
    "Tesla",
    "Cadillac",
    "Mazda",
    "Buick",
    "Chrysler",
    "Lincoln",
    "Volvo",
    "Acura",
    "Infiniti",
    "Porsche",
    "Land Rover",
    "Jaguar",
    "Mini",
    "Mitsubishi"
]

# @callback(
#     Output(component_id='cars-per-brand-plot', component_property='figure'),
#     Input(component_id='scroll', component_property='value'),
# )
def generate_mpb_bar():
    most_recent_year = df['year'].max()
    temp = df[df['year'] == most_recent_year].groupby(['make', 'fuel_type_1']).count()
    temp = temp.reset_index().iloc[:, :3]
    temp.columns = ['make', 'fuel type', 'count']

    temp2 = df[df['year'] == most_recent_year].groupby(['make']).count()
    temp2 = temp2.reset_index().iloc[:, :2]
    temp2.columns = ['make', 'total_count']
    temp = temp.merge(temp2, on='make').sort_values(by=['total_count'])
    temp = temp[temp['make'].isin(popular_car_brands_us)]
    fig = px.bar(temp,
                y='make',
                x='count',
                color='fuel type',
                title=f'Number of Models Per Brand ({most_recent_year})',
                hover_data='total_count',
                category_orders={'make': temp['make'].tolist()[::-1],
                                 'fuel type': ['Regular Gasoline', 'Midgrade Gasoline', 'Premium Gasoline', 'Diesel', 'Electricity']},
                color_discrete_sequence=px.colors.qualitative.D3,
                )
    fig.update_layout(
        font=dict(
                    size=14  # Set the font size to 14
                ),
        #plot_bgcolor='#111111',
        paper_bgcolor='#f0f0f0',
        margin=dict(t=60)
    )
    fig.update_yaxes(tickmode='linear', dtick=1)
    fig.update_layout(showlegend=False)

    return fig



layout = html.Div([
    html.Div('This is our Archive page content.'),
])