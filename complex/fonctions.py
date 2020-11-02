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


def multi_form(x: Union[int, float], y: Union[int, float], ttype: str) -> dict:
    """
    return cartesian and polor form of complex number as a dict
    Parameters
    ----------
    x : Union[int, float]
    y : Union[int, float]
    ttype : str

    Returns
    -------
    dict
    """
    if x is None:
        x = 0
    if y is None:
        y = 0

    if ttype == "Polar":
        r = x
        phi = y
        x = r * math.cos(phi)
        y = r * math.sin(phi)
    elif ttype == "Cartesian":
        r = math.sqrt((x ** 2 + y ** 2))
        if r + x == 0:
            phi = math.pi
        else:
            phi = 2 * math.atan(y / (r + x))
    else:
        raise NotImplementedError("pls, only use Polar or Cartesian")
    return {"x": x, "y": y, "r": r, "phi": phi}


def ellipse_arc(
    x_center: Union[int, float] = 0,
    y_center: Union[int, float] = 0,
    a: Union[int, float] = 1,
    b: Union[int, float] = 1,
    start_angle: Union[int, float] = 0,
    end_angle: Union[int, float] = 2 * np.pi,
) -> str:
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

    Returns
    -------
    str
    """
    t = np.linspace(start_angle, end_angle, 60)
    x = x_center + a * np.cos(t)
    y = y_center + b * np.sin(t)
    path = f"M {x[0]}, {y[0]}"
    for k in range(1, len(t)):
        path += f"L{x[k]}, {y[k]}"
    return path


def figure_creator(
    x: Union[int, float], y: Union[int, float], ttype: str, fanboy: bool = False
) -> go.Figure:
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
    data = multi_form(x, y, ttype)
    x = data["x"]
    y = data["y"]
    r = data["r"]
    phi = data["phi"]

    fig = go.Figure()

    fig.update_layout(
        width=900,
        height=900,
        xaxis_range=[-r * 2, r * 2],
        yaxis_range=[-r * 2, r * 2],
        shapes=[
            dict(
                type="path",
                path=ellipse_arc(a=r * 0.1, b=r * 0.1, start_angle=0, end_angle=phi),
                line_color="Blue",
            )
        ],
    )
    fig.update_xaxes(range=[-r * 1.4, r * 1.4], zeroline=False)
    fig.update_yaxes(range=[-r * 1.4, r * 1.4])
    fig.add_shape(
        type="circle", xref="x", yref="y", x0=-r, y0=-r, x1=r, y1=r, line_color="Black",
    )
    fig.add_shape(type="line", x0=0, y0=0, x1=x, y1=y, line=dict(color="red", width=4,))
    fig.add_shape(
        type="line", x0=0, y0=0, x1=0, y1=y, line=dict(color="MediumPurple", width=2)
    )
    fig.add_shape(
        type="line", x0=0, y0=0, x1=x, y1=0, line=dict(color="MediumBlue", width=2)
    )
    fig.add_shape(
        type="line",
        x0=0,
        y0=y,
        x1=x,
        y1=y,
        line=dict(color="MediumPurple", width=2, dash="dot",),
    )
    fig.add_shape(
        type="line",
        x0=x,
        y0=0,
        x1=x,
        y1=y,
        line=dict(color="MediumBlue", width=2, dash="dot",),
    )
    fig.add_trace(
        go.Scatter(
            x=[x * 1.2, x * 0.2],
            y=[y * 1.2, -y * 0.1],
            text=[
                f"x = {x}, y = {y}i",
                f"{round(phi, 3)}pi, {round(math.degrees(phi), 3)}°",
            ],
            mode="text",
        )
    )
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
                layer="below",
            )
        )

    return fig
