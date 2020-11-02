import math
from copy import deepcopy
from typing import Union
from .web_server.main import RunItStepBro
from complex.fonctions import figure_creator, multi_form


class Complex:
    """
    My complex function :D
    """

    def __init__(
        self,
        a: Union[int, float, None] = None,
        b: Union[int, float, None] = None,
        ttype: str = "Cartesian",
        easy_load: bool = False,
    ) -> None:
        """ initialise Complex
        create self.__real and self.__im aka real part and imaginary part of the complex number
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
        if easy_load:
            getter_gui = RunItStepBro()
            if getter_gui.data["type"] == "Cartesian":
                self.__real = getter_gui.data["x"]
                self.__im = getter_gui.data["y"]
            elif getter_gui.data["type"] == "Polar":
                self.__real = getter_gui.data["x"] * math.cos(getter_gui.data["y"])
                self.__im = getter_gui.data["x"] * math.sin(getter_gui.data["y"])
                self.__arg = getter_gui.data["y"]
                self.__module = getter_gui.data["x"]
        else:
            data = multi_form(a, b, ttype)
            self.__real = data["x"]
            self.__im = data["y"]
            self.__arg = data["r"]
            self.__module = data["phi"]

    """ getters """

    @property
    def real(self) -> Union[int, float]:
        """
        Returns deepcopy of self.__real

        Returns
        -------
         Union[int, float]
        """
        return deepcopy(self.__real)

    @property
    def im(self) -> Union[int, float]:
        """
        Returns deepcopy of self.__real

        Returns
        -------
         Union[int, float]
        """
        return deepcopy(self.__im)

    @property
    def arg(self) -> Union[int, float]:
        """
        return deepcopy of self.__arg
        Returns
        -------
        Union[int, float]
        """
        return deepcopy(self.__arg)

    @property
    def module(self) -> Union[int, float]:
        """
        return deepcopy of self.__module
        Returns
        -------
        Union[int, float]
        """
        return deepcopy(self.__module)

    @property
    def conj(self) -> "Complex":
        """
        Returns conjugates

        Returns
        -------
        "Complex"
        """
        return Complex(a=self.__real, b=-self.__im, ttype="Cartesian")

    @property
    def get_arg(self) -> Union[int, float]:
        """
        Returns arguments

        Returns
        -------
        Union[int, float]

        """
        if self.__arg is not None:
            return self.__arg
        raise NotImplementedError("I'm bad at Maths :/")

    @property
    def get_module(self) -> Union[int, float]:
        """
        Returns module

        Returns
        -------
        Union[int, float]

        """
        if self.__module is not None:
            return self.__module
        return math.sqrt((self.__real ** 2 + self.__im ** 2))

    """ setters """

    """NO SETTERS NEEDED"""

    """ methods """

    def __add__(self, other: Union[int, float, "Complex"]) -> "Complex":
        """

        Parameters
        ----------
        other : Union[int, float, Complex]

        Returns
        -------
        "Complex"

        """
        if isinstance(other, (int, float)):
            return Complex(self.__real + other, self.__im + other, ttype="Cartesian")
        elif isinstance(other, Complex):
            return Complex(self.__real + other.real, self.__im + other.__im, ttype="Cartesian")
        else:
            raise NotImplementedError(f"Type : {type(other)} is not supported")

    def __sub__(self, other: Union[int, float, "Complex"]) -> "Complex":
        """

        Parameters
        ----------
        other : Union[int, float, Complex]

        Returns
        -------
        "Complex"

        """
        if isinstance(other, (int, float)):
            return Complex(self.__real - other, self.__im - other, ttype="Cartesian")
        elif isinstance(other, Complex):
            return Complex(self.__real - other.real, self.__im - other.__im, ttype="Cartesian")
        else:
            raise NotImplementedError(f"Type : {type(other)} is not supported")

    def __mul__(self, other: Union[int, float, "Complex"]) -> "Complex":
        """

        Parameters
        ----------
        other : Union[int, float, Complex]

        Returns
        -------
        "Complex"

        """
        if isinstance(other, (int, float)):
            return Complex(self.__real * other, self.__im * other, ttype="Cartesian")
        elif isinstance(other, Complex):
            a = self.__real * other.real - self.__im * other.__im
            b = self.__real * other.__im + self.__im * other.real
            return Complex(a=a, b=b, ttype="Cartesian")
        else:
            raise NotImplementedError(f"Type : {type(other)} is not supported")

    def __truediv__(self, other: Union[int, float, "Complex"]) -> "Complex":
        """

        Parameters
        ----------
        other : Union[int, float, Complex]

        Returns
        -------
        "Complex"

        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError
            self.__real /= other
            self.__im /= other
            return Complex(self.__real / other, self.__im / other, ttype="Cartesian")
        elif isinstance(other, Complex):
            if other.real + other.__im == 0:
                raise ZeroDivisionError
            top = self * other
            bot = other.real ** 2 + other.__im ** 2
            return Complex(top.__real / bot, top.__im / bot, ttype="Cartesian")
        else:
            raise NotImplementedError(f"Type : {type(other)} is not supported")

    def show(self) -> None:
        fig = figure_creator(self.__real, self.__im, ttype="Cartesian")
        fig.show()

    def __str__(self) -> str:
        if self.__im < 0:
            return f"{self.__real}{self.__im}i "
        else:
            return f"{self.__real}+{self.__im}i "

    def __rtruediv__(self, other) -> None:
        raise NotImplementedError("Not implemented yet")

    __floordiv__ = __truediv__
    __radd__ = __add__
    __rsub__ = __sub__
    __rfloordiv__ = __truediv__
