import dash
from dash import dcc, html, callback, Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os
import json

dash.register_page(__name__, name="Women&Enterprise", order=1)

# Define the color pallete
color1 = '#555B6E'  # Payne's Gray (cinzento escuro)
color2 = '#FFD6BA'  # Apricot (laranja)
color3 = '#BEE3DB'  # Mint Green
color4 = '#89B0AE'  # Cambridge Blue
color5 = '#FAF9F9'  # Seasalt
map_colors = ["#b3efe2", "#1f7a67"]

data_gender_statistics_path = os.path.abspath(os.path.join(os.getcwd(), "assets", "Data_Gender_Statistics.xlsx"))
countries_curiosities_path = os.path.abspath(os.path.join(os.getcwd(), "assets", "countries_Curiosities.json"))
data_gender_statistics = pd.read_excel(data_gender_statistics_path)

data_gender_statistics = data_gender_statistics.rename(columns={
    'Employment to population ratio, 15+, female (%) (national estimate)': 'Female Employment to population ratio (%)',
    'Female share of employment in senior and middle management (%)': 'Female % in senior and middle management',
    'Labor force with advanced education, female (% of female working-age population with advanced education)': 'Advanced Education (% of female)',
    'Labor force with basic education, female (% of female working-age population with basic education)': 'Basic Education (% of female)',
    'Labor force with intermediate education, female (% of female working-age population with intermediate education)': 'Intermediate Education (% of female)',
    'Labor force with advanced education, male (% of male working-age population with advanced education)': 'Advanced Education (% of male)',
    'Labor force with basic education, male (% of male working-age population with basic education)': 'Basic Education (% of male)',
    'Labor force with intermediate education, male (% of male working-age population with intermediate education)': 'Intermediate Education (% of male)',
    'Law mandates equal remuneration for females and males for work of equal value (1=yes; 0=no)': 'Law mandates wages equality',
    'Population, total': 'Total Population',
    'Share of female business owners (% of total business owners)': 'Female Business Owners (%)',
    'Share of female directors (% of total directors)': 'Female directors (%)',
    'Share of female sole proprietors  (% of sole proprietors)': 'Female Sole Proprietors (%)'
})

# open and read the countries curiosities json file
with open(countries_curiosities_path, 'r') as file:
    countries_curiosities = json.load(file)


year_to_filter=2020
map_graph = px.choropleth(data_gender_statistics.loc[data_gender_statistics['Year'] == year_to_filter],
                          locations='Country Name',
                          color='Total Population',
                          color_continuous_scale=map_colors,
                          range_color=(0, 90000000),
                          scope="europe",
                          locationmode="country names",
                          # projection='natural earth',
                          fitbounds='locations',
                          hover_name="Country Name",
                          hover_data={"Country Name": False,"Total Population":False},
                          )
map_graph.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                        paper_bgcolor=color5,
                        plot_bgcolor=color5,
                        font_family="Roboto",
                        font_color=color1,
                        legend_font_size=10,
                        font_size=15,
                        autosize=True,
                        width=835,
                        height=658,
                        showlegend=False,
                        geo={"projection": {"type": "natural earth"}, "bgcolor": 'rgba(0,0,0,0)'},
                        coloraxis_colorbar={
                            "len": 0.7,  # adjust height of colorbar
                            "title": {"text": "Total Population"},  # set colorbar title orientation
                            "title_font": {"size": 15},
                            "tickfont": {"size": 15}
                        },
                        dragmode=False
                        )
map_graph.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations",
                      projection_rotation=dict(lon=0, lat=0, roll=0), lataxis_range=[38, 50], lonaxis_range=[38, 50])


layout = dbc.Container(
    [
        dbc.Row(html.P("Exploring Entrepreneurship along European Union",className="chart-title"),
                style={"padding-top":"32px","padding-left": "12px"}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='mapGraph', figure=map_graph, className="map"),
                    width=8),
            dbc.Col([
                dbc.Row(html.Div(id="country_text"),className="h-50",style={"padding-bottom":"30px"}),
                dcc.Graph(id='table', className="table")],
                width=4)
        ])
    ]
)

def map10ToYesNo(x):
    if x==1:
        return "Yes"
    else:
        return "No"


@callback(
    Output(component_id='table', component_property='figure'),
    Output(component_id='country_text', component_property='children'),
    [Input(component_id='mapGraph', component_property='hoverData')]
)
def callback_table(hover_data):
    if hover_data is None:
        country = "Portugal";
    else:
        country = hover_data['points'][0]['location']

    country_data = data_gender_statistics[(data_gender_statistics["Country Name"] == country) & (data_gender_statistics["Year"] == year_to_filter)]

    population = country_data["Total Population"].values[0]/1000000
    # Create a dictionary of the features and their values
    features = {
        "Total Population (M)": f"{population:.2f}",
        "Female Business Owners (%)": f"{country_data['Female Business Owners (%)'].values[0]:.2f}",
        "Female directors (%)": f"{country_data['Female directors (%)'].values[0]:.2f}",
        "Female Sole Proprietors (%)": f"{country_data['Female Sole Proprietors (%)'].values[0]:.2f}",
        "Law mandates wages equality": map10ToYesNo(country_data["Law mandates wages equality"].values[0])
    }

    fig = go.Figure(data=[go.Table(
        columnwidth=[100, 40],
        header=dict(values=["<b>" + country + "</b>", "<b>" + str(year_to_filter) + "</b>"], line_color=color5,
                    fill_color=color3,
                    font_color=color1,font_size=15),
        cells=dict(values=[
            list(features.keys()),
            list(features.values())
        ], line_color="#f3f1f1", fill_color="#f3f1f1", align="left", font_family="Roboto",font_color=color1,font_size=15,height=24
        )
    )
    ])
    fig.update_layout(autosize=True,height=154,margin=dict(l=0, r=0, t=0, b=0))
    return fig,countries_curiosities[country];
















