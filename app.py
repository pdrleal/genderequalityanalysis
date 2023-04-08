import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

external_stylesheets = ['assets/style.css']
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX,external_stylesheets])
server = app.server
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "13rem",
    "padding": "2rem 1rem",
    "background-color": "#f3f1f1",
    "font-family": "Roboto",
    "color": "#555B6E",
    "text-align":"left"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "13rem",
    "background-color": '#FAF9F9',
    "font-family": "Roboto",
    "color": "#555B6E"
}

sidebar = html.Div(
    [
        html.H2("Gender Equality Analysis", className="display-8", style={"color": "#555B6E"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(page['name'], href=page['path'], active="exact")
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            style={"font-size": "15px"}),
        html.Hr(),
        html.P("Despite the progress accomplished in recent years comparing with the rest of the globe, "
               "Gender Inequality remains an issue in Europe. Women are still underrepresented in leadership "
               "positions and continue to face significant disparities in wages and employment opportunities.",
               style= {"text-align":"justify","font-size":"14px"})
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div(
    [
        sidebar,
        # content of each page
        html.Div(dash.page_container, style=CONTENT_STYLE)
    ],
    style={"background-color": '#FAF9F9'})

if __name__ == "__main__":
    app.run(debug=True)
