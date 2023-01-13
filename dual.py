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

    def __pos__(self):
        return self

    def __neg__(self):
        return Dual(-self.real, -self.dual)

    def conj(self):
        return Dual(self.real, -self.dual)

    def __abs__(self):
        return Dual(abs(self.real), abs(self.dual))

    def __add__(self, y):
        try:
            return Dual(self.real + y.real, self.dual + y.dual)
        except AttributeError:
            return Dual(self.real + y, self.dual)

    def __radd__(self, y):
            return Dual(self.real + y, self.dual)

    def __sub__(self, y):
        try:
            return Dual(self.real - y.real, self.dual - y.dual)
        except AttributeError:
            return Dual(self.real - y, self.dual)

    def __rsub__(self, y):
        return Dual(y - self.real, -self.dual)

    def __mul__(self, y):
        try:
            return Dual(self.real * y.real, (self.real * y.dual) + (self.dual * y.real))
        except AttributeError:
            return Dual(self.real * y, self.dual * y)

    def __rmul__(self, y):
        return Dual(self.real * y, self.dual*y)

    def __eq__(self, y):
        try:
            return self.real == y.real and self.dual == y.dual
        except AttributeError:
            return self.real == y

    def __pow__(self, y):
        """ x**y """

        # this is tricky
        # (x + dx)^(y + dy) ~= x^y + x^(y - 1) * (y * dx + x * log(x) * dy)
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

        if self.real == 0 and y.real >= 1:
            if y.real > 1:
                return Dual(0,0);
            else:
                return self;

        if self.real < 0 and y == math.floor(y.real):
            tmp = y.real * math.pow(self.real, y.real - 1)
            return Dual(math.pow(self.real, y.real), tmp * self.dual)
        else:
            tmp1 = math.pow(self.real, y.real)
            tmp2 = y.real * math.pow(self.real, y.real - 1)
            tmp3 = tmp1 * math.log(self.real)
            return Dual(tmp1, tmp2 * self.dual + tmp3 * y.dual)

    def __rpow__(self, y):
        # y**x, if expression is 3 ** Dual(4),then x = Dual(4), y = 3
        real = y ** self.real
        return Dual(real, real*(self.dual * math.log(y.real)))

    def __truediv__(self, y):
        y_real_inv = 1. / y.real
        try:
            real_div = self.real * y_real_inv
            return Dual(real_div, (self.dual - real_div*y.dual) * y_real_inv)
        except AttributeError:
            return Dual(self.real * y_real_inv, self.dual * y_real_inv)
        
    def __rtruediv__(self, y):
        y = Dual(y, 0)
        return y / self

    def __hash__(self):
        return hash(self.real + self.dual*1j) # use builtin hash for complex

    def __repr__(self):
        if self.dual >= 0:
            return f'{self.real} + {self.dual}ε'
        else:
            return f'{self.real} - {-self.dual}ε'

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

