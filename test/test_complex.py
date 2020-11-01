import pytest
from complex.complex_main import Complex
import math
from typing import Union


@pytest.mark.parametrize(
    "a ,b,r,phi,mode,res",
    [
        (1, 1, None, None, "real", 1),
        (1, 1, None, None, "im", 1),
        (-1, -1, None, None, "real", -1),
        (-1, -1, None, None, "im", -1),
        (0, 0, None, None, "real", 0),
        (0, 0, None, None, "im", 0),
        (None, None, None, None, "im", "ERROR"),
        (None, None, 2, 0, "real", 2),
        (None, None, 2, math.pi / 2, "im", 2),
    ],
)
def test_complex_meth(
    a: Union[int, float, None],
    b: Union[int, float, None],
    r: Union[int, float, None],
    phi: Union[int, float, None],
    mode: str,
    res: Union[Complex, int, float],
):
    if res == "ERROR":
        with pytest.raises((ZeroDivisionError, ValueError)):
            Complex(a, b, r, phi)
    else:
        comp = Complex(a, b, r, phi)
        assert getattr(comp, mode) == res


@pytest.mark.parametrize(
    "comp1,comp2,op,mode,res",
    [
        (Complex(1, 1), Complex(1, 1), "+", "real", Complex(2, 2)),
        (Complex(2, 2), Complex(2, 2), "*", "im", Complex(0, 8)),
    ],
)
def test_complex_op(
    comp1: Complex, comp2: Complex, op: str, mode: str, res: Complex,
):
    if op == "+":
        if res == "ERROR":
            with pytest.raises((ZeroDivisionError, ValueError)):
                compt = getattr((comp1 + comp2), mode)
        else:
            assert getattr((comp1 + comp2), mode) == getattr(res, mode)
    elif op == "-":
        if res == "ERROR":
            with pytest.raises((ZeroDivisionError, ValueError)):
                compt = getattr((comp1 - comp2), mode)
        else:
            assert getattr((comp1 - comp2), mode) == getattr(res, mode)
    elif op == "*":
        if res == "ERROR":
            with pytest.raises((ZeroDivisionError, ValueError)):
                compt = getattr((comp1 * comp2), mode)
        else:
            assert getattr((comp1 * comp2), mode) == getattr(res, mode)
    elif op == "/":
        if res == "ERROR":
            with pytest.raises((ZeroDivisionError, ValueError)):
                compt = getattr((comp1 / comp2), mode)
        else:
            assert getattr((comp1 / comp2), mode) == getattr(res, mode)
