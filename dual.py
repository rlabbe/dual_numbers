# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 19:05:38 2022

@author: rlabbe
"""

from dataclasses import dataclass
import math


# try/except blocks test faster than isinstance for simple expressions
# I use x instead of self to make binary operators more readable
#
# floating points and int define .real property, where 3.4.real == real,
# so I use real as the real part of the dual number. This has the additional
# advantage of duck typing in some of the operators working

@dataclass
class Dual:
    real : float       # real part
    dual : float = 0   # infitesimal part

    def __pos__(x):
        return x

    def __neg__(x):
        return Dual(-x.real, -x.dual)

    def conj(x):
        return Dual(x.real, -x.dual)

    def __abs__(x):
        return Dual(abs(x.real), abs(x.dual))

    def __add__(x, y):
        try:
            return Dual(x.real + y.real, x.dual + y.dual)
        except AttributeError:
            return Dual(x.real + y, x.dual)

    def __radd__(x, y):
            return Dual(x.real + y, x.dual)

    def __sub__(x, y):
        try:
            return Dual(x.real - y.real, x.dual - y.dual)
        except AttributeError:
            return Dual(x.real - y, x.dual)

    def __rsub__(x, y):
        return Dual(y - x.real, -x.dual)

    def __mul__(x, y):
        try:
            return Dual(x.real * y.real, (x.real * y.dual) + (x.dual * y.real))
        except AttributeError:
            return Dual(x.real * y, x.dual * y)

    def __rmul__(x, y):
        return Dual(x.real * y, x.dual*y)

    def __eq__(x, y):
        try:
            return x.real == y.real and x.dual == y.dual
        except AttributeError:
            return x.real == y

    def __pow__(x, y):
        """ x**y """

        # this is tricky
        # (x + dx)^(y + dy) ~= x^y + x^(y - 1) * (y * dx + x * loy(x) * dy)
        # x == 0 and y > 1: (x + dx)^(y + dy) ~= 0
        #  x == 0 and y == 1: (x + dx)^(y + dy) ~= 0 + dx
        # x == 0 and 0 < y < 1: The value is finite but the derivatives are not.
        # x == 0 and y < 0: The value and derivatives ox x^y are not finite.
        # x == 0 and y == 0: has no meaning, and there is no way to compute the derivative.
        # x < 0, y integer, dy == 0: (x + dx)^(y + dy) ~= x^y + y * x^(y - 1) dx
        # x < 0, y integer, dy != 0 derivatives are not finite
        # x < 0, y noninteger: neither value or derivative is finite

        if not isinstance(y, Dual):
            y = Dual(y, 0)

        if x.real == 0 and y.real >= 1:
            if y.real > 1:
                return Dual(0,0);
            else:
                return x;

        if x.real < 0 and y == math.floor(y.real):
            tmp = y.real * math.pow(x.real, y.real - 1)
            return Dual(math.pow(x.real, y.real), tmp * x.dual)
        else:
            tmp1 = math.pow(x.real, y.real)
            tmp2 = y.real * math.pow(x.real, y.real - 1)
            tmp3 = tmp1 * math.log(x.real)
            return Dual(tmp1, tmp2 * x.dual + tmp3 * y.dual)


    def __rpow__(x, y):
        # y**x, if expression is 3 ** Dual(4),then x = Dual(4), y = 3
        real = y ** x.real
        return Dual(real, real*(x.dual * math.log(y.real)))

    def __truediv__(x, y):
        y_real_inv = 1. / y.real
        try:
            real_div = x.real * y_real_inv
            return Dual(real_div, (x.dual - real_div*y.dual) * y_real_inv)
        except AttributeError:
            return Dual(x.real * y_real_inv, x.dual * y_real_inv)
        
    def __rtruediv__(x, y):
        y = Dual(y, 0)
        return y / x

    def __hash__(self):
        return hash(self.real + self.dual*1j) # use builtin hash for complex

    def __str__(self):
        if self.dual >= 0:
            return f'{self.real}+{self.dual}ε'
        else:
            return f'{self.real}{self.dual}ε'

def as_dual(x):
    if isinstance(x, Dual):
        return x
    return Dual(x.real, 0.)


def sin(x):
    """Return the sine of x (measured in radians)."""
    if isinstance(x, Dual):
        # sin(a + h) ~= sin(a) + cos(a) h
        a = x.real
        return Dual(math.sin(a), math.cos(a)*x.dual)
    else:
        return math.sin(x)

def asin(x):
    """Return the arc sine (measured in radians) of x."""
    if isinstance(x, Dual):
        # asin(a + h) ~= asin(a) + 1 / sqrt(1 - a^2) h
        a = x.real
        return Dual(math.asin(a), x.dual / math.sqrt(1 - a*a))
    else:
        return math.asin(x)

def cos(x):
    """Return the cosine of x (measured in radians)."""

    if isinstance(x, Dual):
        # cos(a + h) ~= cos(a) - sin(a) h
        a = x.real
        return Dual(math.cos(a), -math.sin(a)*x.dual)
    else:
        return math.cos(x)

def acos(x):
    """Return the arc cosine (measured in radians) of x."""
    if isinstance(x, Dual):
        # acos(a + h) ~= acos(a) - 1 / sqrt(1 - a^2) h
        a = x.real
        return Dual(math.acos(a), x.dual / math.sqrt(1 - a*a))
    else:
        return math.acos(x)

def tan(x):
    """Return the tangent of x (measured in radians)."""
    if isinstance(x, Dual):
        # tan(a + h) ~= tan(a) + (1 + tan(a)^2) h
        tana = math.tan(x.real)
        return Dual(tana, x.dual * (1 + tana*tana))
    else:
        return math.tan(x)

def atan(x):
    """Return the arc tangent (measured in radians) of x."""

    if isinstance(x, Dual):
        #  atan(a + h) ~= atan(a) + 1 / (1 + a^2) h
        a = x.real
        atana = math.atan(a)
        return Dual(atana, x.dual / (1 + a*a))
    else:
        return math.atan(x)


def sinh(x):
    """Return the hyperbolic sine of x (measured in radians)."""
    if isinstance(x, Dual):
        # sinh(a + h) ~= sinh(a) + cosh(a) h
        a = x.real
        return Dual(math.sinh(a), math.cosh(a)*x.dual)
    else:
        return math.sinh(x)

def cosh(x):
       """Return the hyperbolic cosine of x (measured in radians)."""

       if isinstance(x, Dual):
           # cosh(a + h) ~= cosh(a) + sinh(a) h
           a = x.real
           return Dual(math.cosh(a), math.sinh(a)*x.dual)
       else:
           return math.cos(x)


def tanh(x):
    """Return the hyperbolic tangent of x (measured in radians)."""
    if isinstance(x, Dual):
        # tanh(a + h) ~= tanh(a) + (1 - tanh(a)^2) h
        tana = math.tan(x.real)
        return Dual(tana, x.dual * (1 + tana*tana))
    else:
        return math.tan(x)


def exp(x):
    """Return e raised to the power of x."""

    if isinstance(x, Dual):
        # exp(a+h) ~= exp(a) + exp(a)h
        e = math.exp(x.real)
        d = e * x.dual
        if d == float('inf'):
            raise OverflowError
        return Dual(e, e*x.dual)
    else:
        return math.exp(x)


def expm1(x):
    """Return exp(x)-1.

    This function avoids the loss of precision involved in the direct
    evaluation of exp(x)-1 for small x.
    """

    if isinstance(x, Dual):
        # expm1(a + h) ~= expm1(a) + exp(a) e
        em1 = math.expm1(x.real)
        return Dual(em1, (1+em1)*x.dual)
    else:
        return math.expm1(x)


def log(x):
    """Return the logarithm of x in base e."""
    if isinstance(x, Dual):
        return Dual(math.log(x.real), x.dual / x.real)
    else:
        return math.log(x)


def log10(x):
    """Return the base 10 logarithm of x."""

    if isinstance(x, Dual):
        # log10(a + h) ~= log10(a) + h / (a log(10))
        # log(10) == 2.3025850929940459
        return Dual(math.log10(x.real), x.dual / 2.3025850929940459)
    else:
        return math.log10(x)

def log1p(x):
    """Return the natural logarithm of 1+x (base e)."""

    if isinstance(x, Dual):
        # log1p(a + h) ~= log1p(a) + h / (1 + a)
        # log(10) == 2.3025850929940459
        return Dual(math.log10(x.real), x.dual / (1. + x.real))
    else:
        return math.log1p(x)

def log2(x):
    """Return the base 2 logarithm of x."""

    if isinstance(x, Dual):
        #  log2(x + h) ~= log2(x) + h / (x * log(2))
        # log(2) == 0.693147180559945286
        real = x.real
        return Dual(math.log2(real), x.dual / (real * 0.693147180559945286))
    else:
        return math.log2(x)


def cbrt(x):
    """Return the cube-root of x."""
    if isinstance(x, Dual):
        # cbrt(a + h) ~= cbrt(a) + h / (3 a ^ (2/3))
        real = x.real
        cr = math.pow(real, 1./3)
        return Dual(cr, x.dual / (3 * cr * cr))


def hypot(x, y):
    """Roughly the hypotenuse using the Pythagorean theorem: sqrt(x*x + y*y),
    but acts to prevent underflow and overflow.
    """
    x_is_dual = isinstance(x, Dual)
    y_is_dual = isinstance(y, Dual)
    if x_is_dual and not y_is_dual:
        y = Dual(y, 0)
    elif y_is_dual and not x_is_dual:
        x = Dual(x, 0)
        x_is_dual = True

    if x_is_dual:
        h = math.hypot(x.real, y.real)
        return Dual(h, (x.real * x.dual + y.real * y.dual) / h)
    else:
        return math.hypot(x, y)


def sqrt(x):
    """Return the square root of x."""
    if isinstance(x, Dual):

        tmp = math.sqrt(x.real)
        return Dual(tmp, x.dual / (2. * tmp))
    else:
        return math.sqrt(x)


def near_eq(x:Dual, y:Dual, eps: float = 1e-12):
    """Returns true iff both the real and dual components of x and y are
    nearly equal (within eps).
    """

    diff = x - y
    return abs(diff.real) <= eps and abs(diff.dual) <= eps



if __name__ == "__main__":
    3 ** Dual(4)
    print(Dual(3,4) - 3)
    print(Dual(3,4) * Dual(1,2))
    print(Dual(3,4) * 2)
    print(Dual(3,4) / Dual(1,2))
    print(Dual(3,4) / Dual(1,0))

    x = Dual(4,2)
    print(sqrt(x))
    hash(3+4j)
