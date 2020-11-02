import pytest
from complex.complex_main import Complex
import math
from typing import Union
from complex.fonctions import multi_form


@pytest.mark.parametrize(
    "x, y, ttype,res",
    [
        (
            1,
            1,
            "Cartesian",
            {"phi": 0.7853981633974484, "r": 1.4142135623730951, "x": 1, "y": 1}
        ),
        (
            1,
            1,
            "Polar",
            {'phi': 1, 'r': 1, 'x': 0.5403023058681398, 'y': 0.8414709848078965}
        ),
        (
            0,
            0,
            "Polar",
            {'phi': 0, 'r': 0, 'x': 0.0, 'y': 0.0}
        ),
        (
            1,
            1,
            "Edd",
            "ERROR"
        )
    ],
)
def test_multi_form(x, y, ttype, res):
    if res == "ERROR":
        with pytest.raises(NotImplementedError):
            tes = multi_form(x, y, ttype)
    else:
        assert multi_form(x, y, ttype) == res
