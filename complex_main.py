import math
from typing import Union
import plotly.express as px


class Complex:
    """
    My complex function :D
    """
    def __init__(
        self,
        a: Union[int, float, None] = None,
        b: Union[int, float, None] = None,
        r: Union[int, float, None] = None,
        phi: Union[int, float, None] = None,
    ) -> None:
        """ initialise l'objet Complex
        create self.real and self.im aka real part and imaginay part of the complex numbre
        ! only use cartesian form or polar !
        Parameter
        ---------
        a: Union[int, float, None]
            real part for cartesian form
        b: Union[int, float, None]
            complex part for cartesian form
        r: Union[int, float, None]
            module
        phi: Union[int, float, None]
            argument
        """
        self.real = None
        self.im = None
        self.arg = None
        self.module = None
        if a is not None and b is not None:
            self.real = a
            self.im = b
        elif r is not None and phi is not None:
            if self.real is not None:
                raise ValueError("pls give only one pair of ags(polar or Cartesian")
            self.real = r * math.cos(phi)
            self.im = r * math.sin(phi)
            self.arg = phi
            self.module = r
        else:
            raise ValueError("pls give polar or Cartesian coordonates")

    def __add__(self, other: Union[int, float]):
        """

        Parameters
        ----------
        other : Union[int, float, Complex]

        Returns
        -------

        """
        if isinstance(other, (int, float)):
            return Complex(self.real + other, self.im + other)
        elif isinstance(other, Complex):
            return Complex(self.real + other.real, self.im + other.im)
        else:
            raise NotImplemented(f"Type : {type(other)} is not supported")

    def __sub__(self, other: Union[int, float]):
        """

        Parameters
        ----------
        other : Union[int, float, Complex]

        Returns
        -------

        """
        if isinstance(other, (int, float)):
            return Complex(self.real - other, self.im - other)
        elif isinstance(other, Complex):
            return Complex(self.real - other.real, self.im - other.im)
        else:
            raise NotImplemented(f"Type : {type(other)} is not supported")

    def __mul__(self, other: Union[int, float]):
        """

        Parameters
        ----------
        other : Union[int, float, Complex]

        Returns
        -------

        """
        if isinstance(other, (int, float)):
            return Complex(self.real * other, self.im * other)
        elif isinstance(other, Complex):
            a = self.real * other.real - self.im * other.im
            b = self.real * other.im + self.im * other.real
            return Complex(a=a, b=b)
        else:
            raise NotImplemented(f"Type : {type(other)} is not supported")

    def __truediv__(self, other: Union[int, float]):
        """

        Parameters
        ----------
        other : Union[int, float, Complex]

        Returns
        -------

        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError
            self.real /= other
            self.im /= other
            return Complex(self.real / other, self.im / other)
        elif isinstance(other, Complex):
            if other.real + other.im == 0:
                raise ZeroDivisionError
            top = self * other
            bot = other.real ** 2 + other.im ** 2
            return Complex(top.real / bot, top.im / bot)
        else:
            raise NotImplemented(f"Type : {type(other)} is not supported")

    def get_conj(self):
        return Complex(a=self.real, b=-self.im)

    def get_arg(self):
        if self.arg is not None:
            return self.arg
        raise NotImplemented("I'm bad at Maths :/")

    def get_module(self):
        if self.module is not None:
            return self.module
        raise NotImplemented("I'm realy bad at Maths :'/")

    def show(self) -> None:
        fig = px.scatter(
            x=[self.real],
            y=[self.im],
            range_x=[-1 + self.real * -2, 1 + self.real * 2],
            range_y=[-1 + self.im * -2, 1 + self.im * 2],
        )
        fig.show()

    def __str__(self) -> str:
        if self.im < 0:
            return f"{self.real}{self.im}i "
        else:
            return f"{self.real}+{self.im}i "

    def __rtruediv__(self, other) -> None:
        raise NotImplemented("Not implemented yet")

    __floordiv__ = __truediv__
    __radd__ = __add__
    __rsub__ = __sub__
    __rfloordiv__ = __truediv__
