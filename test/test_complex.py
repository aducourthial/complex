from typing import Union

import pytest

from complex.complex_main import Complex


@pytest.mark.parametrize(
    "a ,b,ttype,res",
    [
        (1, 1, "Cartesian", (1, 1)),
        (1, 1, "Polar", (0.8414709848078965, 0.5403023058681398)),
        (0, 0, "Cartesian", (0, 0)),
        (1, 0, "Polar", (0, 1)),
        (1, 1, "Cartesian", (1, 1)),

    ],
)
def test_complex_meth(
        a: Union[int, float],
        b: Union[int, float],
        ttype: str,
        res: Union[Complex, int, float]
):
    if res == "ERROR":
        with pytest.raises((ZeroDivisionError, ValueError)):
            Complex(a, b, ttype)
    else:
        comp = Complex(a, b, ttype)
        assert (comp.im, comp.real) == res


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
