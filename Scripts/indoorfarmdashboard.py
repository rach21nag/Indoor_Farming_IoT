import os
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#A3EBB1",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def home_layout():
    # print(os.path.join(os.getcwd(), "smart_farming.jpg"))
    simple_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col([
                                html.H4("INTRODUCTION TO SMART FARMING", className="card-title"),
                                html.P(
                                    "Smart farming has taken a leap from traditional farming as "
                                    "it brings reliability and predictability at our Fingertips. Automation and cloud "
                                    "software cloud software systems are tools for smart farming. Smart farming "
                                    " emphasises on acquiring data collected by sensors and make productive use of it. "
                                    "Smart farming employs hardware (IoT) and software (SaaS) to capture "
                                    "the data and give actionable insights to manage all the operations on the farm. "
                                    "The data is organized, accessible all the time that can be monitored remotely "
                                    "and allows us to take necessary actions. Smart farming analyses soil moisture "
                                    " content, indoor room temperature and humidity and light intensity to get "
                                    "knowledge about suitable crops and water requirements for optimization. In this "
                                    "project, different sensors are used to detect real-time physical conditions like "
                                    "temperature, humidity, light intensity and soil moisture content and send the "
                                    "data to Raspberry Pi. Then, the data will be processed by Raspberry Pi "
                                    "and uploaded to the Cloud. Furthermore, the system will automatically maintain "
                                    "ambient conditions by modulating HVAC devices, indoor lighting and water pumps "
                                    "to save energy. The web-based application aims to graphically represent "
                                    "the gathered data to provide better understanding of the facility "
                                    "With the help of indoor farming using HVAC and IoT, productivity and "
                                    "quality of crops are expected to increase significantly. Additionally, "
                                    "reduction of carbon footprints is also achieved.",
                                    className="card-text",
                                )], width=10),
                            dbc.Col([
                                html.H6("        ", className="card-title"),
                                html.H6("PROCESS", className="card-title"),
                                html.P(
                                        "Sensors : Temperature and Humidity Sensor (DHT11), Light sensor (LDR), "
                                        "Soil Moisture Sensor (Capacitive Sensor Module V1.2). " 
                                        "Actuators : Stepper motor (HVAC Cooler), Stepper motor (Water pump), "
                                        "LEDs (Lights).      "
                                        "Plant: Fenugreek",
                                    className="card-text",
                                )], width=10),

                        ]

                    )

                ]
            ),
        ]
    )
    image_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Row(
                        [

                            dbc.Col(
                                html.Img(src=app.get_asset_url('vertfarming.jpg'),
                                         style={'height': '80%', 'width': '80%'})),
                            dbc.Col(
                                html.Img(src=app.get_asset_url('vertfarming2.PNG')))
                                         #style={'height': '80%', 'width': '80%'}))
                        ]

                    ),
                    dbc.Row(
                        [

                            dbc.Col(
                                html.Img(src=app.get_asset_url('farmer_sensor.jpg'),
                                         style={'height': '80%', 'width': '80%'})),
                            dbc.Col(
                                html.Img(src=app.get_asset_url('drone_farming.jpg'),
                                         style={'height': '80%', 'width': '80%'}))
                        ]

                    ),
                    # dbc.Row(
                    #     [
                    #
                    #         dbc.Col(
                    #             html.Img(src=app.get_asset_url('smart-farming.jpg'),
                    #                      style={'height': '60%', 'width': '50%'}))
                    #     ]
                    #
                    # )

                ]
            ),
        ]
    )

    row = dbc.Row(
        [
            dbc.Col(simple_card, width=12),
            dbc.Col(image_card, width=12)
        ]
    )

    return row


def plant1_layout():
    df1 = pd.read_csv('iotdata.csv')

    fig1 = px.line(df1, x="Time", y="Temperature")
    fig2 = px.line(df1, x="Time", y="Humidity")
    fig3 = px.line(df1, x="Time", y="Light")
    fig4 = px.line(df1, x="Time", y="Moisture")
    fig5 = px.line(df1, x="Time", y="Light Energy")
    fig6 = px.line(df1, x="Time", y="Pump Energy")
    row = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(
                        id='example-graph-1',
                        figure=fig1
                    ), width=12),
                    dbc.Col(dcc.Graph(
                        id='example-graph-2',
                        figure=fig2
                    ), width=12),
                    dbc.Col(dcc.Graph(
                        id='example-graph-3',
                        figure=fig3
                    ), width=12),
                    dbc.Col(dcc.Graph(
                        id='example-graph-4',
                        figure=fig4
                    ), width=12),
                    dbc.Col(dcc.Graph(
                        id='example-graph-5',
                        figure=fig5
                    ), width=12),
                    dbc.Col(dcc.Graph(
                        id='example-graph-6',
                        figure=fig6
                    ), width=12),
                ]
            ),
        ]
    )

    return row


sidebar = html.Div(
    [
        html.H2("Indoor Farming", className="display-4"),
        html.Hr(),
        html.P(
            "Click on the links to view in details", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Plant 1", href="/page-1", active="exact"),
                dbc.NavLink("Plant 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home_layout()
    elif pathname == "/page-1":
        return plant1_layout()
        # return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is plant 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
