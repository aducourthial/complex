import math
from typing import Union

import dash
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from flask import request
import numpy as np

RET = {}
external_stylesheets = ["https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def ellipse_arc(x_center: Union[int, float] = 0, y_center: Union[int, float] = 0, a: Union[int, float] = 1,
                b: Union[int, float] = 1, start_angle: Union[int, float] = 0, end_angle: Union[int, float] = 2 * np.pi,
                N: Union[int, float] = 60) -> str:
    """
    mostly from : https://community.plotly.com/t/arc-shape-with-path/7205/5

    Parameters
    ----------
    x_center: Union[int, float]
    y_center: Union[int, float]
    a: Union[int, float]
    b: Union[int, float]
    start_angle: Union[int, float]
    end_angle: Union[int, float]
    N: Union[int, float]

    Returns
    -------
    str
    """
    t = np.linspace(start_angle, end_angle, N)
    x = x_center + a * np.cos(t)
    y = y_center + b * np.sin(t)
    path = f'M {x[0]}, {y[0]}'
    for k in range(1, len(t)):
        path += f'L{x[k]}, {y[k]}'
    return path


def figure_creator(x: Union[int, float], y: Union[int, float], ttype: str, fanboy: bool = False) -> go.Figure:
    """
    Argand Diagram creator

    Parameters
    ----------
    fanboy : bool
        wink wink
    x : Union[int, float]
    y : Union[int, float]
    ttype : str

    Returns
    -------

    go.Figure
    """
    if ttype == "Polar":
        r = x
        x1 = x * math.cos(y)
        y = x * math.sin(y)
        x = x1
    else:
        r = math.sqrt((x ** 2 + y ** 2))
        if r + x == 0:
            phi = math.pi
        else:
            phi = 2 * math.atan(y / (r + x))

    fig = go.Figure(layout={"height": 900, "width": 900})

    fig.update_layout(width=900, height=900,
                      xaxis_range=[-r * 2, r * 2],
                      yaxis_range=[-r * 2, r * 2],
                      shapes=[
                          dict(type="path",
                               path=ellipse_arc(a=r * 0.1, b=r * 0.1, start_angle=0, end_angle=phi),
                               line_color="Blue")
                      ]
                      )
    fig.update_xaxes(range=[-r * 1.4, r * 1.4], zeroline=False)
    fig.update_yaxes(range=[-r * 1.4, r * 1.4])
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=-r, y0=-r, x1=r, y1=r,
                  line_color="Black",
                  )
    fig.add_shape(type="line",
                  x0=0, y0=0, x1=x, y1=y,
                  line=dict(
                      color="red",
                      width=4,
                  ))
    fig.add_shape(type="line",
                  x0=0, y0=0, x1=0, y1=y,
                  line=dict(
                      color="MediumPurple",
                      width=2
                  ))
    fig.add_shape(type="line",
                  x0=0, y0=0, x1=x, y1=0,
                  line=dict(
                      color="MediumBlue",
                      width=2
                  ))
    fig.add_shape(type="line",
                  x0=0, y0=y, x1=x, y1=y,
                  line=dict(
                      color="MediumPurple",
                      width=2,
                      dash="dot",
                  ))
    fig.add_shape(type="line",
                  x0=x, y0=0, x1=x, y1=y,
                  line=dict(
                      color="MediumBlue",
                      width=2,
                      dash="dot",
                  ))
    fig.add_trace(go.Scatter(
        x=[x * 1.2, x * 0.2],
        y=[y * 1.2, -y * 0.1],
        text=[f"x = {x}, y = {y}i", f"{round(phi, 3)}pi, {round(math.degrees(phi), 3)}°"],
        mode="text",
    ))
    if fanboy:
        fig.add_layout_image(
            dict(
                source="https://avatars1.githubusercontent.com/u/59824904?s=400&u=bc3e4149dcbfe011f1a7484576d08c66a9aeb6df&v=4",
                xref="x",
                yref="y",
                x=-r,
                y=r,
                sizex=2 * r,
                sizey=2 * r,
                sizing="stretch",
                opacity=0.5,
                layer="below")
        )

    return fig


fig = go.Figure(layout={"height": 900, "width": 900})


def shutdown():
    """
    Shutdown Flask server
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


app.layout = html.Div(className="container-fluid", id="mainp", children=[dcc.Store(id='memory'),
                                                                         html.Div(className="row", children=[
                                                                             html.Div(className="col", children=[
                                                                                 html.H1(
                                                                                     children='Complex Object Creator 2.0'),
                                                                                 dcc.Dropdown(
                                                                                     id='dropdown',
                                                                                     options=[
                                                                                         {'label': 'Cartesian',
                                                                                          'value': 'Cartesian'},
                                                                                         {'label': 'Polar',
                                                                                          'value': 'Polar'},
                                                                                         {'label': 'Exp',
                                                                                          'value': 'Exp'}
                                                                                     ],
                                                                                     value='Cartesian'
                                                                                 ),
                                                                                 dcc.Input(id="x", type="number",
                                                                                           placeholder="Entre real part"),
                                                                                 dcc.Input(id="y", type="number",
                                                                                           placeholder="Entre im part"),
                                                                                 html.Button('Save Complex ?',
                                                                                             id='submit-val',
                                                                                             n_clicks=0),
                                                                                 dcc.Checklist(id="ff",
                                                                                               options=[
                                                                                                   {'label': 'fanboy',
                                                                                                    'value': 'fanboy'}]
                                                                                               )
                                                                             ]),
                                                                             html.Div(className="col", children=[
                                                                                 dcc.Graph(id='Complex', figure=fig)
                                                                             ])
                                                                         ])
                                                                         ])


@app.callback(dash.dependencies.Output("Complex", "figure"),
              [dash.dependencies.Input('x', 'value'),
               dash.dependencies.Input('y', 'value')],
              [dash.dependencies.State("dropdown", "value"),
              dash.dependencies.State('ff',"value")])
def update_fig(x: Union[int, float], y: Union[int, float], type_e: str, fb: list) -> str:
    """
    callback to update fig when input modified

    Parameters
    ----------
    fb : list
        wink wink
    x : Union[int, float]
    y : Union[int, float]
    type_e : str

    Returns
    -------
    str
    """
    if fb == ["fanboy"]:
        fb = True
    else:
        fb = False
    if x is None or y is None:
        raise PreventUpdate
    return figure_creator(x, y, type_e, fb)


@app.callback([dash.dependencies.Output("x", "placeholder"), dash.dependencies.Output("y", "placeholder")],
              dash.dependencies.Input('dropdown', 'value'))
def update_input(on_dp):
    if on_dp == "Cartesian":
        return "Entre real part", "Entre im part"
    elif on_dp == 'Polar':
        return "Entre arg", "Entre phi"
    else:
        return 'entre somthinf', "lol"


@app.callback(dash.dependencies.Output("mainp", "children"),
              dash.dependencies.Input('submit-val', 'n_clicks'),
              [dash.dependencies.State("x", "value"),
               dash.dependencies.State("y", "value"),
               dash.dependencies.State("dropdown", "value")])
def update_output(n_clicks: int, x: Union[int, float], y: Union[int, float], ttype: str) -> html.H1:
    """

    Parameters
    ----------
    n_clicks : int
    x : Union[int, float]
    y : Union[int, float]
    ttype : str

    Returns
    -------
    html.H1
    """
    if n_clicks == 0:
        raise PreventUpdate
    else:
        RET["x"] = x
        RET["y"] = y
        RET["type"] = ttype
        shutdown()
        return html.H1("PLS close the page")


class RunItStepBro:
    """
    well, hello
    """

    def __init__(self):
        app.run_server()
        self.data = RET
