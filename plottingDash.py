import pandas as pd
import plotly
import plotly.subplots

from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc


# SETTINGS IN ARDUINO SKETCH
baudrate = 9600                     # bits/sec
delayBetweenMeasurements = 1000     # ms

# SYSTEM SETTINGS
port = 'COM3'

# DATA FILES
realtimeData = 'realtimeData.txt'
calibData = 'calibrationdata.txt'


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        html.Div(
            children=[

                html.H1(children="Monitoring soil moisture", className='header-title'),
                html.P(
                    children=(
                        "Equipment: The Arduino Uno board and a capacitive soil moisture sensor."
                    ),
                    className='header-description'
                ),
            ],
            className='header',
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(id='get_calibration'),
                    className='card',
                ),

                html.Div(
                    children=dcc.Graph(id='live-update-graph'),
                    className='card',
                ),
                html.Div(
                    children=dcc.Interval(
                        id='interval-component',
                        interval=delayBetweenMeasurements, # in milliseconds
                        n_intervals=0
                    ),
                    className='card',
                ),
            ],
            className='wrapper',
        ),
    ]
)

@callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):

    data = pd.read_csv(realtimeData, names=['time', 'sensorData'], delimiter='\t', skiprows=1)

    figure = plotly.subplots.make_subplots(rows=1, cols=1)
    figure.append_trace({
                         "x": data['time'],
                         "y": data['sensorData'],
                         "name" : 'sensor measurements',
                         'mode': 'lines+markers',
                        'type': 'scatter',
                        'marker_color' : 'black'
                        },1,1)

    figure.update_layout(
        title={
            'text': 'Real-time measurement',
            'x': 0.5,
            'xanchor': 'center'
        })

    return format_figure(figure)


@callback(Output('get_calibration', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_calibration(n):
    data = pd.read_csv(calibData, names=['labels','moisture'],delimiter='\t')

    figure = plotly.subplots.make_subplots(rows=1, cols=1)
    figure.append_trace({
                         "x": data["labels"],
                         "y": data["moisture"],
                         "name" : 'calibration',
                         'mode': 'markers',
                        'type': 'scatter',
                        'marker_color' : 'black',
                        },1,1)

    figure.update_layout(
        title={
            'text': 'Calibration',
            'x': 0.5,
            'xanchor': 'center'
        })

    return format_figure(figure)


def format_figure(figure):

    figure.add_shape(type="rect",
                  xref="paper", yref="paper",
                  x0=0, y0=(450-150)/(500-150),
                  x1=1, y1=1,
                  line=dict(
                      color="#FC666F",
                      width=1,
                  ),
                  fillcolor="#FC666F", opacity=0.2
                  )

    figure.add_shape(type="rect",
                     xref="paper", yref="paper",
                     x0=0, y0=(200-150) / (500 - 150),
                     x1=1, y1=(450 - 150) / (500 - 150),
                     line=dict(
                         color="#5CE084",
                         width=1,
                     ),
                     fillcolor="#5CE084", opacity=0.2
                     )

    figure.add_shape(type="rect",
                  xref="paper", yref="paper",
                  x0=0, y0=0,
                  x1=1, y1=(200-150) / (500 - 150),
                  line=dict(
                      color="#FC666F",
                      width=1,
                  ),
                  fillcolor="#FC666F", opacity=0.2
                  )

    figure.update_layout(
        plot_bgcolor='white'
    )
    figure.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    figure.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )

    figure.update_layout(yaxis_title='moisture [-]',
                         yaxis_range=[150, 500])
    return figure


if __name__ == "__main__":
    app.run_server(debug=True)