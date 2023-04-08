import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_daq as daq
from PIL import Image, ImageOps
import io, base64, os
from plotly.subplots import make_subplots
import numpy as np

dash.register_page(__name__, path='/', name="Historical Overview", order=0)

# Define the color pallete
color1 = '#555B6E'  # Payne's Gray (cinzento escuro)
color2 = '#FFD6BA'  # Apricot (laranja)
color3 = '#BEE3DB'  # Mint Green
color4 = '#89B0AE'  # Cambridge Blue
color5 = '#FAF9F9'  # Seasalt
map_colors = [color1, color2, color3, color4, color5]

data_gender_statistics_path = os.path.abspath(os.path.join(os.getcwd(), "assets", "Data_Gender_Statistics.xlsx"))
data_gender_wages_path = os.path.abspath(os.path.join(os.getcwd(), "assets", "Data_Gender_Wages.xlsx"))
data_gender_statistics = pd.read_excel(data_gender_statistics_path)

data_gender_statistics = data_gender_statistics.rename(columns={
    'Employment to population ratio, 15+, female (%) (national estimate)': 'Female Employment to population ratio (%)',
    'Employment to population ratio, 15+, male (%) (national estimate)': 'Male Employment to population ratio (%)',
    'Female share of employment in senior and middle management (%)': 'Female % in senior and middle management',
    'Labor force with advanced education, female (% of female working-age population with advanced education)': 'Advanced Education (% of female)',
    'Labor force with basic education, female (% of female working-age population with basic education)': 'Basic Education (% of female)',
    'Labor force with intermediate education, female (% of female working-age population with intermediate education)': 'Intermediate Education (% of female)',
    'Labor force with advanced education, male (% of male working-age population with advanced education)': 'Advanced Education (% of male)',
    'Labor force with basic education, male (% of male working-age population with basic education)': 'Basic Education (% of male)',
    'Labor force with intermediate education, male (% of male working-age population with intermediate education)': 'Intermediate Education (% of male)',
    'Law mandates equal remuneration for females and males for work of equal value (1=yes; 0=no)': 'Law mandates wages equality',
    'Population ages 15-64, total': 'Total Population(15-64 years old)'
})

data_gender_wages = pd.read_excel(data_gender_wages_path)

layout = dbc.Container(
    [
        dbc.Row([
            dbc.Row([
                html.Div([
                    html.P("Choose one EU country to explore:", style={"padding-left": "12px",
                                                                       "padding-bottom": "15px",
                                                                       "font-size": "20px"}),
                    dcc.Dropdown(
                        id="selected_country_main",
                        options=[x for x in data_gender_statistics['Country Name'].unique()],
                        value="Portugal", style={"margin-bottom": "20px", "width": "200px", "font-size": "20px",
                                                 'border-radius': '10px',
                                                 'border-color': color3,
                                                 # "border":"none",
                                                 'cursor': 'pointer',
                                                 "background-color": color5},
                        clearable=False,
                    )
                ], style={"display": "flex"})
                , html.Hr()
            ], style={"padding-top": "32px"}),
            dbc.Col([
                dbc.Row([
                    html.P("Select the date:", style={"padding-bottom": "15px", "padding-top": "20px"}),
                    daq.Slider(
                        id="date_slider",
                        min=data_gender_statistics['Year'].min(),
                        max=data_gender_statistics['Year'].max(),
                        step=1,
                        marks={i: '{}'.format(i) for i in
                               range(data_gender_statistics['Year'].min(), data_gender_statistics['Year'].max() + 1,
                                     10)},
                        value=data_gender_statistics['Year'].max(),
                        dots=False,
                        color=color1,
                        updatemode="drag",
                        size=370,
                        handleLabel={"showCurrentValue": True, "label": "Year"},
                    )
                ], style={"padding-left": "20px"}),
                dbc.Row([
                    html.P("Labor Force Participation by Gender", className="chart-title",
                           style={"padding-top": "100px"}),
                    html.P("Percentage of women/men who are employed in the total population of working age.",
                           style={"font-size": "14px", "opacity": "60%", "padding-bottom": "30px",
                                  "text-align": "justify"}),
                    dbc.Col(
                        html.P(id="label_perc_w", style={"color": color3, "font-weight": "bold", "font-size": "30px",
                                                         "text-align": "center", "padding-top": "40px"})),
                    dbc.Col(html.Div(id="filled-women", className="person-icon-left")),
                    dbc.Col(html.Div(id="filled-men", className="person-icon-right")),
                    dbc.Col(
                        html.P(id="label_perc_m", style={"color": color2, "font-weight": "bold", "font-size": "30px",
                                                         "text-align": "center", "padding-top": "40px"}))
                ], style={"padding": "0px", "margin": "0px"}),
                dbc.Row([
                    html.P("Women Business and the Law Index Score", className="chart-title",
                           style={"padding-top": "80px"}),
                    html.P(
                        "Assess how laws and regulations affect women’s economic opportunity based on the indicators: "
                        "Mobility, Workplace, Pay, Marriage, Parenthood, Entrepreneurship, Assets and Pension.",
                        style={"font-size": "14px", "opacity": "60%", "padding-bottom": "30px",
                               "text-align": "justify"}),
                    dcc.Graph(id="gaugeChart")], style={"padding-left": "12px"}),
                dbc.Row([
                    html.P("Women Involvement in Leadership", className="chart-title", style={
                        "padding-top": "80px"}),
                    html.P("Percentage of women in total employment who hold high level managerial positions and "
                           "Percentage of parliamentary seats in a single or lower chamber held by women.",
                           style={"font-size": "14px", "opacity": "60%", "padding-bottom": "30px",
                                  "text-align": "justify"}),
                    dbc.Col([
                        dcc.Graph(id="pieChart1"),
                        html.P("Women in Senior and Middle Management",
                               style={"padding-top": "10px", "font-size": "14px", "text-align": "center"})
                    ]),
                    dbc.Col([
                        dcc.Graph(id="pieChart2"),
                        html.P("Women in National Parliaments",
                               style={"padding-top": "10px", "font-size": "14px", "text-align": "center"})
                    ])
                ], style={"padding-left": "12px", "padding-bottom": "80px"}),
            ], width=4),
            dbc.Col([
                dbc.Row([
                    html.P("Gender Pay Gap at a Glance", className="chart-title", style={"padding-left": "90px",
                                                                                         "padding-top": "20px"}),
                    html.P("Highlighting the salaries inequalities faced by women in the job-market.",
                           style={"font-size": "14px", "opacity": "60%", "padding-left": "90px",
                                  "padding-bottom": "30px", "text-align": "left"}),
                    dbc.Row([dcc.Graph(id='gapChart')], style={"padding-left": "100px"})
                ], style={"padding-bottom": "35px"}),
                dbc.Row([

                    html.P("The Growth of Women Participation in Labor Force",
                           className="chart-title",
                           style={"padding-left": "90px", "padding-right": "10px"}),
                    html.Div([
                        html.P("Change in the percentage of women who are employed in the total "
                               "population of working age over the period of 2000 to 2020.",
                               style={"font-size": "14px", "opacity": "60%", "padding-left": "90px",
                                      "padding-bottom": "30px", "text-align": "justify", "width": "600px"}),
                        dbc.RadioItems(
                            id='top-last',
                            className='radio',
                            options=[dict(label='Top 15', value=0), dict(label='Last 15', value=1)],
                            value=0,
                            inline=True
                        )
                    ], style={"display": "inline-flex", "padding-top": "12px","padding-left": "0px"}),

                    dbc.Row(dcc.Graph(id='growth_chart'), style={"padding-left": "100px"})])
            ], style={"padding-bottom": "35px"}, width=8)
        ]),
        dbc.Row([
            dbc.Col([
                html.P("Education Level Impact on Labor Force", className="chart-title",
                       style={"padding-left": "12px"}),
                html.P("Percentage of men/women in the labor force who have attained a determined level of education.",
                       style={"font-size": "14px", "opacity": "60%", "padding-left": "12px",
                              "text-align": "justify"}),
                dbc.Row(dcc.Graph(id='educationChart'), style={"padding-left": "22px", "padding-top": "30px"})
            ], width=9, style={"padding-bottom": "30px"}),
            dbc.Col([
                html.P("First select which type of Education you want to explore:", style={"padding-top": "81px",
                                                                                           "padding-bottom": "5px"}),
                dcc.Dropdown(
                    id="selected_education",
                    options=[x for x in ["Basic", "Intermediate", "Advanced"]],
                    value="Advanced", style={"width": "200px",
                                             "font-size": "16px",
                                             'border-radius': '10px',
                                             "color": "#555B6E",
                                             'border-color': color3,
                                             'cursor': 'pointer',
                                             "background-color": color5},
                    clearable=False,
                ),
                html.P("Second, add another Country to the analysis:", style={"padding-top": "30px",
                                                                              "padding-bottom": "5px"}),
                dcc.Dropdown(
                    id="selected_country_secondary",
                    options=[x for x in data_gender_statistics['Country Name'].unique()],
                    value=None, style={"width": "200px",
                                       "font-size": "16px",
                                       'border-radius': '10px',
                                       'border-color': color3,
                                       'cursor': 'pointer',
                                       "background-color": color5},
                    clearable=True,
                ),
                html.P("Finally, select one or both Genders:", style={"padding-top": "30px",
                                                                      "padding-bottom": "5px"}),
                dbc.Checklist(id="selected_gender", options=['Female', 'Male'], value=['Female'],
                              switch=True, inline=True)
            ], width=3)
        ])
    ], fluid=True)


@callback(Output("filled-women", "children"),
          Output("label_perc_w", "children"),
          Output("filled-men", "children"),
          Output("label_perc_m", "children"),
          [Input(component_id='selected_country_main', component_property='value'), Input("date_slider", "value")])
def update_figures_fill(selected_country_main, date_slider):
    default_woman = Image.open("assets/women-figure.png")
    default_man = Image.open("assets/men-figure.png")

    df_overall = data_gender_statistics[
        (data_gender_statistics['Country Name'] == selected_country_main) & (
                data_gender_statistics['Year'] == date_slider)]
    woman_percentage = round(df_overall['Female Employment to population ratio (%)'].values[0], 1)
    man_percentage = round(df_overall['Male Employment to population ratio (%)'].values[0], 1)
    # Women cropping
    filled_woman = Image.open("assets/women-figure-filled.png")
    width_woman, height_woman = filled_woman.size
    # Calculate the height of the top percentage of the image
    top_height_woman = int(height_woman * (1 - woman_percentage / 100))
    # Crop the image to the top percentage
    filled_woman_cropped = filled_woman.crop((0, top_height_woman, width_woman, height_woman))

    woman_figure = default_woman.copy()
    woman_figure.paste(filled_woman_cropped, (0, top_height_woman))

    # Man cropping
    filled_man = Image.open("assets/men-figure-filled.png")
    width_man, height_man = filled_man.size
    # Calculate the height of the top percentage of the image
    top_height_man = int(height_man * (1 - man_percentage / 100))
    # Crop the image to the top percentage
    filled_man_cropped = filled_man.crop((0, top_height_man, width_man, height_man))

    man_figure = default_man.copy()
    man_figure.paste(filled_man_cropped, (0, top_height_man))

    # Convert to html Image
    woman_buffer = io.BytesIO()
    woman_figure.save(woman_buffer, format='PNG')
    img_str_woman = base64.b64encode(woman_buffer.getvalue()).decode('utf-8')
    woman_figure = html.Img(src='data:image_wpman/png;base64,' + img_str_woman, height="120px")

    man_buffer = io.BytesIO()
    man_figure.save(man_buffer, format='PNG')
    img_str_man = base64.b64encode(man_buffer.getvalue()).decode('utf-8')
    man_figure = html.Img(src='data:image_man/png;base64,' + img_str_man, height="120px")

    return woman_figure, str(woman_percentage) + "%", man_figure, str(man_percentage) + "%";


@callback(
    Output(component_id='gaugeChart', component_property='figure'),
    [Input(component_id='selected_country_main', component_property='value'),
     Input(component_id='date_slider', component_property='value')]
)
def callback_gauge_chart(selected_country_main, date_slider):
    data_temp = data_gender_statistics[
        (data_gender_statistics['Country Name'] == selected_country_main) & (
                data_gender_statistics['Year'] == date_slider)]
    average = np.round(data_gender_statistics.loc[
                           data_gender_statistics['Year'] == date_slider, 'Women Business and the Law Index Score '
                                                                          '(scale 1-100)'].mean(), 2)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=data_temp['Women Business and the Law Index Score (scale 1-100)'].values[0],
        delta={'reference': average, 'increasing': {'color': color1}, 'decreasing': {'color': color3}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 0.5, 'tickcolor': color1},
            'bar': {'color': color3},
            'bgcolor': color5,
            'borderwidth': 2,
            'bordercolor': color1,
            'threshold': {
                'line': {'color': color1, 'width': 10},
                'thickness': 0.5,
                'value': average}}
    ))
    fig.update_layout(autosize=True,
                      height=155,
                      #       width=360,
                      margin=dict(l=30, r=35, t=25, b=20),
                      xaxis_title='Year',
                      yaxis_title='% of Female/ Male',
                      paper_bgcolor=color5,
                      plot_bgcolor=color1,
                      font_family="Roboto",
                      font_color=color1,
                      legend_font_size=10,
                      font_size=15
                      )
    return fig;


@callback(
    Output(component_id='pieChart1', component_property='figure'),
    Output(component_id='pieChart2', component_property='figure'),
    [Input(component_id='selected_country_main', component_property='value'),
     Input(component_id='date_slider', component_property='value')]
)
def callback_pie_charts(selected_country_main, date_slider):
    data_temp = data_gender_statistics[
        (data_gender_statistics['Country Name'] == selected_country_main) & (
                data_gender_statistics['Year'] == date_slider)]
    percent_management = np.round(data_temp['Female % in senior and middle management'].values[0], 1)
    percent_management_text = str(percent_management) + "%"
    percent_parliament = np.round(data_temp['Proportion of seats held by women in national parliaments (%)'].values[0],
                                  1)
    percent_parliament_text = str(percent_parliament) + "%"

    if pd.isna(percent_management):
        percent_management = 0;
        percent_management_text = "NAD"
    if pd.isna(percent_parliament):
        percent_parliament = 0;
        percent_parliament_text = "NAD"

    fig1 = go.Figure(go.Pie(
        values=[percent_management, 100 - percent_management],  # Set the values for the filled and empty portions
        hole=.6,  # Set the size of the hole in the center of the donut
        showlegend=False,  # Hide the legend
        textinfo='none',  # Hide the percentage labels
        sort=False,
        marker=dict(colors=[color3, color1])
    ))

    fig1.update_layout(
        annotations=[dict(
            text=percent_management_text,  # Set the percentage text
            x=0.5,  # Set the x-position of the text (0.5 is the center)
            y=0.5,  # Set the y-position of the text (0.5 is the center)
            showarrow=False,  # Hide the arrow
            font=dict(size=22, color=color1)
        )],
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor=color5,
        font_family="Roboto",
        height=180,
        width=180
    )

    fig2 = go.Figure(go.Pie(
        values=[percent_parliament, 100 - percent_parliament],  # Set the values for the filled and empty portions
        hole=.6,  # Set the size of the hole in the center of the donut
        showlegend=False,  # Hide the legend
        textinfo='none',  # Hide the percentage labels
        marker=dict(colors=[color3, color1]),  # Set the colors for the filled and empty portions
        sort=False
    ))

    fig2.update_layout(
        annotations=[dict(
            text=percent_parliament_text,  # Set the percentage text
            x=0.5,  # Set the x-position of the text (0.5 is the center)
            y=0.5,  # Set the y-position of the text (0.5 is the center)
            showarrow=False,  # Hide the arrow
            font=dict(size=22, color=color1)
        )],
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor=color5,
        font_family="Roboto",
        autosize=False,
        height=180,
        width=180
    )
    return fig1, fig2;


@callback(
    Output(component_id='gapChart', component_property='figure'),
    [Input(component_id='selected_country_main', component_property='value')]
)
def callback_gap_chart(selected_country_main):
    data_temp = data_gender_wages[(data_gender_wages['Country'] == selected_country_main) &
                                  (data_gender_wages['Year'].isin(np.arange(2000, 2021)))]
    fig = px.scatter(data_temp,
                     x='Year',
                     y='Wage',
                     color='Gender',
                     color_discrete_sequence=[color2, color3],
                     hover_data=None)
    fig.update_traces(hovertemplate=None, hoverinfo='skip', marker={'size': 12})

    grouped = data_temp.groupby('Year')
    for year, data in grouped:
        women_wage = data_temp[(data_temp['Gender'] == 'Female') & (data_temp['Year'] == year)]['Wage'].values
        man_wage = data_temp[(data_temp['Gender'] == 'Male') & (data_temp['Year'] == year)]['Wage'].values

        if len(women_wage) == 0 or pd.isnull(women_wage[0]):
            continue

        wage_gap_diff = man_wage[0] - women_wage[0]

        fig.add_trace(go.Scatter(
            x=[year, year],
            y=[women_wage[0],
               man_wage[0]],
            mode='lines',
            line=dict(color=color1),
            showlegend=False,
            hovertemplate=f"<b>Year:</b> {year}<br>"
                          + f"<b>Women's Wage:</b> {women_wage[0]:.2f}<br>"
                          + f"<b>Men's Wage:</b> {man_wage[0]:.2f}<br>"
                          + f"<b>Wage Gap Diff:</b> {wage_gap_diff:.2f}<extra></extra>'"
        ))

    fig.update_layout(hovermode='x',
                      autosize=False,
                      width=700,
                      height=500,
                      paper_bgcolor=color5,
                      plot_bgcolor=color5,
                      font_family="Roboto",
                      font_color=color1,
                      legend_title_font_color=color1,
                      legend_title_font_size=15,
                      legend_font_size=15,
                      font_size=15,
                      margin=dict(l=0, r=0, t=0, b=0),
                      legend=dict(yanchor="top", y=0.99, xanchor='left', x=0.03))
    fig.update_xaxes(title_font_size=20)
    fig.update_yaxes(title_font_size=20)
    return fig;


@callback(
    Output(component_id='growth_chart', component_property='figure'),
    [Input(component_id='top-last', component_property='value')]
)
def callback_education_chart(toplast):
    aux = data_gender_statistics[data_gender_statistics['Year'].isin([2020, 2000])]

    # get the index of the minimum and maximum values of the Year column for each group
    idxmin = aux.groupby('Country Code')['Year'].idxmin()
    idxmax = aux.groupby('Country Code')['Year'].idxmax()

    # use loc to extract the Employment to population ratio for the Year_min and Year_max
    filtered_aux = pd.DataFrame({
        'Country': aux.loc[idxmin, 'Country Code'].values,
        'Country Name': aux.loc[idxmin, 'Country Name'].values,
        'Year_min': aux.loc[idxmin, 'Year'].values,
        'Employment to population ratio_min': aux.loc[
            idxmin, 'Female Employment to population ratio (%)'].values,
        'Year_max': aux.loc[idxmax, 'Year'].values,
        'Employment to population ratio_max': aux.loc[
            idxmax, 'Female Employment to population ratio (%)'].values
    })

    filtered_aux['Growth'] = (filtered_aux['Employment to population ratio_max'] - filtered_aux[
        'Employment to population ratio_min']) / (filtered_aux['Employment to population ratio_min']) * 100

    filtered_aux = filtered_aux.sort_values(by='Growth', ascending=False, ignore_index=True)
    if toplast == 0:
        filtered_aux = filtered_aux.head(15)
    elif toplast == 1:
        filtered_aux = filtered_aux.tail(15)

    growth_chart = go.Figure(go.Bar(
        x=filtered_aux['Growth'],
        y=filtered_aux['Country'],
        customdata=filtered_aux['Country Name'],
        marker=dict(
            color=color3,
            line=dict(
                color=color3,
                width=0.9),
        ),
        orientation='h',
        text=filtered_aux['Growth'].apply(lambda x: f'{x:.2f}'),
        # add percentage values as text
        textposition='outside',  # set the position of the text to be outside the bars
        textfont=dict(
            size=10.5,  # set the font size
        ),
        hovertemplate=None,
        hoverinfo='skip'
    ))

    growth_chart.update_layout(
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0, 1],
            autorange='reversed'
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=False,
            domain=[0, 1],
            title="Percentage Growth in female employment to population ratio (%)"
        ),
        autosize=False,
        width=700,
        height=500,
        paper_bgcolor=color5,
        plot_bgcolor=color5,
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis_title='Country',
        font_family="Roboto",
        font_color=color1,
        legend_font_size=10,
        font_size=15
    )
    return growth_chart;


@callback(
    Output(component_id='educationChart', component_property='figure'),
    [Input(component_id='selected_country_main', component_property='value'),
     Input(component_id='selected_country_secondary', component_property='value'),
     Input(component_id='selected_education', component_property='value'),
     Input(component_id='selected_gender', component_property='value')]
)
def callback_education_chart(selected_country_main, selected_country_secondary, selected_education, selected_gender):
    selected_countries = [selected_country_main, selected_country_secondary]
    selected_gender = list(map(lambda x: x.lower(), selected_gender))

    data_temp = data_gender_statistics[(data_gender_statistics['Year'].isin(np.arange(2000, 2021)))]

    fig = go.Figure()
    dash = None;
    # Current Country
    for country in selected_countries:
        if country is not None:
            for gender in selected_gender:
                series_name = selected_education + " Education (% of " + gender + ")"
                data_temp_line = data_temp[data_temp['Country Name'] == country][series_name]
                color_line = color2
                if gender == "female":
                    color_line = color3
                fig.add_trace(go.Scatter(x=data_temp['Year'], y=data_temp_line,
                                         line=dict(color=color_line, width=2, dash=dash),
                                         name=series_name + " - " + country))
        dash = "dash"

    # title = 'Evolution of Basic and Advanced Education in Country A and Country B',
    fig.update_layout(xaxis_title='Year',
                      yaxis_title='% of Female/ Male',
                      xaxis_range=[1998.5, 2021.5],
                      autosize=False,
                      width=900,
                      height=500,
                      legend=dict(yanchor="top", y=1.2, xanchor='center', x=0.5),
                      margin=dict(l=0, r=0, t=0, b=0),
                      paper_bgcolor=color5,
                      plot_bgcolor=color5,
                      font_family="Roboto",
                      font_color=color1,
                      legend_title_font_color=color1,
                      legend_title_font_size=20,
                      legend_font_size=15,
                      font_size=15
                      )
    return fig;
