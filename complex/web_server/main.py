from typing import Union

import dash
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from flask import request
from complex.fonctions import figure_creator

RET = {}
external_stylesheets = [
    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = go.Figure(layout={"height": 900, "width": 900})


def shutdown():
    """
    Shutdown Flask server
    """
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


app.layout = html.Div(
    className="container-fluid",
    id="mainp",
    children=[
        dcc.Store(id="memory"),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col",
                    children=[
                        html.H1(children="Complex Object Creator 2.0"),
                        dcc.Dropdown(
                            id="dropdown",
                            options=[
                                {"label": "Cartesian", "value": "Cartesian"},
                                {"label": "Polar", "value": "Polar"},
                                {"label": "Exp", "value": "Exp"},
                            ],
                            value="Cartesian",
                        ),
                        dcc.Input(id="x", type="number", placeholder="Entre real part"),
                        dcc.Input(id="y", type="number", placeholder="Entre im part"),
                        html.Button("Save Complex ?", id="submit-val", n_clicks=0),
                        dcc.Checklist(
                            id="ff", options=[{"label": "fanboy", "value": "fanboy"}]
                        ),
                    ],
                ),
                html.Div(
                    className="col", children=[dcc.Graph(id="Complex", figure=fig)]
                ),
            ],
        ),
    ],
)


@app.callback(
    dash.dependencies.Output("Complex", "figure"),
    [dash.dependencies.Input("x", "value"), dash.dependencies.Input("y", "value")],
    [
        dash.dependencies.State("dropdown", "value"),
        dash.dependencies.State("ff", "value"),
    ],
)
def update_fig(
    x: Union[int, float], y: Union[int, float], type_e: str, fb: list
) -> go.Figure:
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


@app.callback(
    [
        dash.dependencies.Output("x", "placeholder"),
        dash.dependencies.Output("y", "placeholder"),
    ],
    dash.dependencies.Input("dropdown", "value"),
)
def update_input(on_dp):
    if on_dp == "Cartesian":
        return "Entre real part", "Entre im part"
    elif on_dp == "Polar":
        return "Entre arg", "Entre phi"
    else:
        raise NotImplementedError("what is exp bro ?")


@app.callback(
    dash.dependencies.Output("mainp", "children"),
    dash.dependencies.Input("submit-val", "n_clicks"),
    [
        dash.dependencies.State("x", "value"),
        dash.dependencies.State("y", "value"),
        dash.dependencies.State("dropdown", "value"),
    ],
)
def update_output(
    n_clicks: int, x: Union[int, float], y: Union[int, float], ttype: str
) -> html.H1:
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
