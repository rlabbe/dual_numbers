# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 18:26:24 2022

@author: rlabbe
"""

import math
import dual
from dual import Dual, sqrt, near_eq, sin, cos, tan, log, exp
import pytest


def test_unitary():
    x = -Dual(3, 1)
    y = Dual(1, 2)
    assert x + y == Dual(-2, 1)
    assert x.conj() == Dual(-3, 1)

    assert abs(Dual(-3, -4)) == Dual(3, 4)
    assert abs(Dual(-3, 4)) == Dual(3, 4)
    assert abs(Dual(3, -4)) == Dual(3, 4)


def test_init():
    assert Dual(3, 1).real == 3
    assert Dual(3, 1).dual == 1
    assert Dual(3).dual == 0
    assert Dual(3) == 3

    assert Dual(3) == 3
    assert Dual(3) != 3.0000000000001
    assert Dual(3) == Dual(1) + Dual(2)
    assert Dual(3, 5) == Dual(1, 2) + Dual(2, 3)


def test_exp():
    x = Dual(4, 2)
    assert dual.exp(x) == math.e ** x

#############################################################


def test_sqrt():
    assert near_eq(sqrt(Dual(3, 4)), Dual(
        1.73205080756887719, 1.15470053837925168))
    assert near_eq(sqrt(Dual(17, -6)),
                   Dual(4.12310562561766059, -0.727606875108998907))
    assert near_eq(sqrt(Dual(64, -6)), Dual(8, -0.375))
    assert near_eq(sqrt(Dual(64, 0)), Dual(8, 0))
    assert near_eq(sqrt(Dual(1, 0)), Dual(1, 0))
    assert near_eq(sqrt(Dual(0.333333333333333315, 0.66666666666666663)), Dual(
        0.577350269189625731, 0.577350269189625731))
    with pytest.raises((ZeroDivisionError)):
        sqrt(Dual(0, 0.66666666666666663))


def test_pow():
    assert near_eq(pow(Dual(3, 0), Dual(2, 0)), Dual(
        9, 0)), f'{pow(Dual(3, 0), Dual(2, 0))} != Dual(9, 0)'
    assert near_eq(pow(Dual(9, 0), Dual(0.5, 0)), Dual(
        3, 0)), f'{pow(Dual(9, 0), Dual(0.5, 0))} != Dual(3, 0)'
    assert near_eq(pow(Dual(9, 0), Dual(0.333333333333333315, 0)), Dual(2.08008382305190409, 0)
                   ), f'{pow(Dual(9, 0), Dual(0.333333333333333315, 0))} != Dual(2.08008382305190409, 0)'
    assert near_eq(pow(Dual(3, 4), Dual(2, 0)), Dual(9, 24)
                   ), f'{pow(Dual(3, 4), Dual(2, 0))} != Dual(9, 24)'
    assert near_eq(pow(Dual(-3, 4), Dual(2, 0)), Dual(9, -24)
                   ), f'{pow(Dual(-3, 4), Dual(2, 0))} != Dual(9, -24)'
    with pytest.raises((ZeroDivisionError)):
        pow(Dual(-3, 4), Dual(2.5, 0))
    assert near_eq(pow(Dual(0, 0), Dual(2, 0)), Dual(
        0, 0)), f'{pow(Dual(0, 0), Dual(2, 0))} != Dual(0, 0)'
    with pytest.raises((ZeroDivisionError)):
        pow(Dual(0, 0), Dual(0, 0))
    assert near_eq(pow(Dual(0, 0), Dual(1, 0)), Dual(
        0, 0)), f'{pow(Dual(0, 0), Dual(1, 0))} != Dual(0, 0)'
    with pytest.raises((ZeroDivisionError)):
        pow(Dual(0, 0), Dual(0.400000000000000022, 0))
    assert near_eq(pow(Dual(9, 0), Dual(-1, 0)), Dual(0.111111111111111105, 0)
                   ), f'{pow(Dual(9, 0), Dual(-1, 0))} != Dual(0.111111111111111105, 0)'
    assert near_eq(pow(Dual(9, 0.5), Dual(-1, 0)), Dual(0.111111111111111105, -0.00617283950617283916)
                   ), f'{pow(Dual(9, 0.5), Dual(-1, 0))} != Dual(0.111111111111111105, -0.00617283950617283916)'
    assert near_eq(pow(Dual(9, 0.5), Dual(-0.333333333333333315, 0)), Dual(0.480749856769136175, -0.00890277512535437437)
                   ), f'{pow(Dual(9, 0.5), Dual(-0.333333333333333315, 0))} != Dual(0.480749856769136175, -0.00890277512535437437)'


def test_mul():
    assert near_eq((Dual(3, 0)*Dual(4, 0)), Dual(12, 0)
                   ), f'{(Dual(3, 0)*Dual(4, 0))} != Dual(12, 0)'
    assert near_eq((3*Dual(4, 0)), Dual(12, 0)
                   ), f'{3*Dual(4, 0)} != Dual(12, 0)'   
    
    # test multiply by scalar
    assert near_eq(Dual(3,0) * Dual(12, 3), 3 * Dual(12, 3))
    assert near_eq(Dual(3,0) * Dual(12, 3), Dual(12, 3) * 3)

    assert near_eq((Dual(4, 0)*Dual(3, 0)), Dual(12, 0)
                   ), f'{(Dual(4, 0)*Dual(3, 0))} != Dual(12, 0)'
    assert near_eq((Dual(-3, 0)*Dual(4, 0)), Dual(-12, 0)
                   ), f'{(Dual(-3, 0)*Dual(4, 0))} != Dual(-12, 0)'
    assert near_eq((Dual(-3, 0)*Dual(-4, 0)), Dual(12, -0)
                   ), f'{(Dual(-3, 0)*Dual(-4, 0))} != Dual(12, -0)'
    assert near_eq((Dual(3, 0)*Dual(-4, 0)), Dual(-12, 0)
                   ), f'{(Dual(3, 0)*Dual(-4, 0))} != Dual(-12, 0)'
    assert near_eq((Dual(3, 1)*Dual(4, 2)), Dual(12, 10)
                   ), f'{(Dual(3, 1)*Dual(4, 2))} != Dual(12, 10)'
    assert near_eq((Dual(0.299999999999999989, 0.100000000000000006)*Dual(0.400000000000000022, 0.200000000000000011)), Dual(0.119999999999999996, 0.100000000000000006)
                   ), f'{(Dual(0.299999999999999989, 0.100000000000000006)*Dual(0.400000000000000022, 0.200000000000000011))} != Dual(0.119999999999999996, 0.100000000000000006)'
    assert near_eq((Dual(0.299999999999999989, 0.100000000000000006)*Dual(0.400000000000000022, -0.200000000000000011)), Dual(0.119999999999999996, -0.01999999999999999)
                   ), f'{(Dual(0.299999999999999989, 0.100000000000000006)*Dual(0.400000000000000022, -0.200000000000000011))} != Dual(0.119999999999999996, -0.01999999999999999)'
    assert near_eq((Dual(0.299999999999999989, -0.100000000000000006)*Dual(0.400000000000000022, 0.200000000000000011)), Dual(0.119999999999999996, 0.01999999999999999)
                   ), f'{(Dual(0.299999999999999989, -0.100000000000000006)*Dual(0.400000000000000022, 0.200000000000000011))} != Dual(0.119999999999999996, 0.01999999999999999)'
    assert near_eq((Dual(0.299999999999999989, -0.100000000000000006)*Dual(0.400000000000000022, -0.200000000000000011)), Dual(0.119999999999999996, -0.100000000000000006)
                   ), f'{(Dual(0.299999999999999989, -0.100000000000000006)*Dual(0.400000000000000022, -0.200000000000000011))} != Dual(0.119999999999999996, -0.100000000000000006)'
    assert near_eq((Dual(-0.299999999999999989, -0.100000000000000006)*Dual(0.400000000000000022, -0.200000000000000011)), Dual(-0.119999999999999996, 0.01999999999999999)
                   ), f'{(Dual(-0.299999999999999989, -0.100000000000000006)*Dual(0.400000000000000022, -0.200000000000000011))} != Dual(-0.119999999999999996, 0.01999999999999999)'
    assert near_eq((Dual(-0.299999999999999989, -0.100000000000000006)*Dual(-0.400000000000000022, -0.200000000000000011)), Dual(0.119999999999999996, 0.100000000000000006)
                   ), f'{(Dual(-0.299999999999999989, -0.100000000000000006)*Dual(-0.400000000000000022, -0.200000000000000011))} != Dual(0.119999999999999996, 0.100000000000000006)'
    assert near_eq((Dual(0.299999999999999989, -0.100000000000000006)*Dual(-0.400000000000000022, -0.200000000000000011)), Dual(-0.119999999999999996, -0.01999999999999999)
                   ), f'{(Dual(0.299999999999999989, -0.100000000000000006)*Dual(-0.400000000000000022, -0.200000000000000011))} != Dual(-0.119999999999999996, -0.01999999999999999)'
    assert near_eq((Dual(0, 0)*Dual(0.400000000000000022, 0.200000000000000011)), Dual(0, 0)
                   ), f'{(Dual(0, 0)*Dual(0.400000000000000022, 0.200000000000000011))} != Dual(0, 0)'




def test_add():
    assert near_eq((Dual(3, 0)+Dual(4, 0)), Dual(7, 0)
                   ), f'{(Dual(3, 0)+Dual(4, 0))} != Dual(7, 0)'
    assert near_eq((Dual(4, 0)+Dual(3, 0)), Dual(7, 0)
                   ), f'{(Dual(4, 0)+Dual(3, 0))} != Dual(7, 0)'
    assert near_eq((Dual(-3, 0)+Dual(4, 0)), Dual(1, 0)
                   ), f'{(Dual(-3, 0)+Dual(4, 0))} != Dual(1, 0)'
    assert near_eq((Dual(-3, 0)+Dual(-4, 0)), Dual(-7, 0)
                   ), f'{(Dual(-3, 0)+Dual(-4, 0))} != Dual(-7, 0)'
    assert near_eq((Dual(3, 0)+Dual(-4, 0)), Dual(-1, 0)
                   ), f'{(Dual(3, 0)+Dual(-4, 0))} != Dual(-1, 0)'
    assert near_eq((Dual(3, 1)+Dual(4, 2)), Dual(7, 3)
                   ), f'{(Dual(3, 1)+Dual(4, 2))} != Dual(7, 3)'
    assert near_eq((Dual(0.299999999999999989, 0.100000000000000006)+Dual(0.400000000000000022, 0.200000000000000011)), Dual(0.699999999999999956, 0.300000000000000044)
                   ), f'{(Dual(0.299999999999999989, 0.100000000000000006)+Dual(0.400000000000000022, 0.200000000000000011))} != Dual(0.699999999999999956, 0.300000000000000044)'
    
    # test add scalar
    assert near_eq(Dual(3, 0) + Dual(4, 8), 3 + Dual(4, 8))
    assert near_eq(Dual(3, 0) + Dual(4, 8), Dual(4, 8) + 3)

    assert near_eq(Dual(-3, 0) + Dual(4, 8), -3 + Dual(4, 8))
    assert near_eq(Dual(-3, 0) + Dual(4, 8), Dual(4, 8)  -3)

                   
def test_sub():
    assert near_eq((Dual(3, 0)-Dual(4, 0)), Dual(-1, 0)
                   ), f'{(Dual(3, 0)-Dual(4, 0))} != Dual(-1, 0)'
    assert near_eq((Dual(4, 0)-Dual(3, 0)), Dual(1, 0)
                   ), f'{(Dual(4, 0)-Dual(3, 0))} != Dual(1, 0)'
    assert near_eq((Dual(-3, 0)-Dual(4, 0)), Dual(-7, 0)
                   ), f'{(Dual(-3, 0)-Dual(4, 0))} != Dual(-7, 0)'
    assert near_eq((Dual(-3, 0)-Dual(-4, 0)), Dual(1, 0)
                   ), f'{(Dual(-3, 0)-Dual(-4, 0))} != Dual(1, 0)'
    assert near_eq((Dual(3, 0)-Dual(-4, 0)), Dual(7, 0)
                   ), f'{(Dual(3, 0)-Dual(-4, 0))} != Dual(7, 0)'
    assert near_eq((Dual(3, 1)-Dual(4, 2)), Dual(-1, -1)
                   ), f'{(Dual(3, 1)-Dual(4, 2))} != Dual(-1, -1)'
    assert near_eq((Dual(0.299999999999999989, 0.100000000000000006)-Dual(0.400000000000000022, 0.200000000000000011)), Dual(-0.100000000000000033, -0.100000000000000006)
                   ), f'{(Dual(0.299999999999999989, 0.100000000000000006)-Dual(0.400000000000000022, 0.200000000000000011))} != Dual(-0.100000000000000033, -0.100000000000000006)'
    
    assert 3 - Dual(4, 5) == Dual(-1, -5)
    assert 3 - Dual(4, 5) == Dual(3, 0) - Dual(4, 5)


def test_divide():
    assert near_eq((Dual(3, 0)/Dual(4, 0)), Dual(0.75, 0)
                   ), f'{(Dual(3, 0)/Dual(4, 0))} != Dual(0.75, 0)'
    assert near_eq((Dual(4, 0)/Dual(3, 0)), Dual(1.33333333333333326, 0)
                   ), f'{(Dual(4, 0)/Dual(3, 0))} != Dual(1.33333333333333326, 0)'
    assert near_eq((Dual(3, 1)/Dual(4, 1)), Dual(0.75, 0.0625)
                   ), f'{(Dual(3, 1)/Dual(4, 1))} != Dual(0.75, 0.0625)'
    assert near_eq((Dual(3, 1)/Dual(4, 2)), Dual(0.75, -0.125)
                   ), f'{(Dual(3, 1)/Dual(4, 2))} != Dual(0.75, -0.125)'
    assert near_eq((Dual(3, -1)/Dual(4, 2)), Dual(0.75, -0.625)
                   ), f'{(Dual(3, -1)/Dual(4, 2))} != Dual(0.75, -0.625)'
    assert near_eq((Dual(3, -1)/Dual(-4, 2)), Dual(-0.75, -0.125)
                   ), f'{(Dual(3, -1)/Dual(-4, 2))} != Dual(-0.75, -0.125)'
    assert near_eq((Dual(3, -1)/Dual(4, -2)), Dual(0.75, 0.125)
                   ), f'{(Dual(3, -1)/Dual(4, -2))} != Dual(0.75, 0.125)'
    assert near_eq((Dual(0, -1)/Dual(4, -2)), Dual(0, -0.25)
                   ), f'{(Dual(0, -1)/Dual(4, -2))} != Dual(0, -0.25)'
    with pytest.raises((ZeroDivisionError)):
        (Dual(3, -1)/Dual(0, -2))
    assert near_eq((Dual(0, 0)/Dual(4, -2)), Dual(0, 0)
                   ), f'{(Dual(0, 0)/Dual(4, -2))} != Dual(0, 0)'
    with pytest.raises((ZeroDivisionError)):
        (Dual(0, 0)/Dual(0, 0))
    with pytest.raises((ZeroDivisionError)):
        (Dual(4, 0)/Dual(0, 0))
        
    # divide with scalars
    assert near_eq(Dual(7, 3) / 2, Dual(7, 3) / Dual(2, 0))
    assert near_eq(Dual(7, 3) / 2.1, Dual(7, 3) / Dual(2.1, 0))
    assert near_eq(2.1 / Dual(7, 3), Dual(2.1, 0) / Dual(7, 3))


def test_sin():
    assert near_eq(sin(Dual(3.14159265358979312, 0)),
                   Dual(1.22464679914735321e-16, -0))
    assert near_eq(sin(Dual(-3.14159265358979312, 0)),
                   Dual(-1.22464679914735321e-16, -0))
    assert near_eq(sin(Dual(1.57079632679489656, 0)), Dual(1, 0))
    assert near_eq(sin(Dual(-1.57079632679489656, 0)), Dual(-1, 0))
    assert near_eq(sin(Dual(-0.785398163397448279, 0)),
                   Dual(-0.707106781186547573, 0))
    assert near_eq(sin(Dual(0, 0)), Dual(0, 0))
    assert near_eq(sin(Dual(3.14159265358979312, 1)),
                   Dual(1.22464679914735321e-16, -1))
    assert near_eq(sin(Dual(-3.14159265358979312, 1)),
                   Dual(-1.22464679914735321e-16, -1))
    assert near_eq(sin(Dual(1.57079632679489656, 1)),
                   Dual(1, 6.12323399573676604e-17))
    assert near_eq(sin(Dual(-1.57079632679489656, 1)),
                   Dual(-1, 6.12323399573676604e-17))
    assert near_eq(sin(Dual(-0.785398163397448279, 1)),
                   Dual(-0.707106781186547573, 0.707106781186547573))
    assert near_eq(sin(Dual(0, 1)), Dual(0, 1))
    assert near_eq(sin(Dual(3.14159265358979312, 0.100000000000000006)), Dual(
        1.22464679914735321e-16, -0.100000000000000006))
    assert near_eq(sin(Dual(-3.14159265358979312, 0.100000000000000006)),
                   Dual(-1.22464679914735321e-16, -0.100000000000000006))
    assert near_eq(sin(Dual(1.57079632679489656, 0.100000000000000006)), Dual(
        1, 6.12323399573676634e-18))
    assert near_eq(sin(Dual(-1.57079632679489656, 0.100000000000000006)),
                   Dual(-1, 6.12323399573676634e-18))
    assert near_eq(sin(Dual(-0.785398163397448279, 0.100000000000000006)),
                   Dual(-0.707106781186547573, 0.0707106781186547656))
    assert near_eq(sin(Dual(0.299999999999999989, 0.299999999999999989)), Dual(
        0.295520206661339546, 0.286600946737681772))
    assert near_eq(sin(Dual(-0.299999999999999989, 0.299999999999999989)),
                   Dual(-0.295520206661339546, 0.286600946737681772))
    assert near_eq(sin(Dual(0.299999999999999989, -0.299999999999999989)),
                   Dual(0.295520206661339546, -0.286600946737681772))
    assert near_eq(sin(Dual(-0.299999999999999989, -0.299999999999999989)),
                   Dual(-0.295520206661339546, -0.286600946737681772))
    assert near_eq(sin(Dual(0, 1)), Dual(0, 1))
    assert near_eq(cos(Dual(3.14159265358979312, 0)), Dual(-1, -0))
    assert near_eq(cos(Dual(-3.14159265358979312, 0)), Dual(-1, 0))
    assert near_eq(cos(Dual(1.57079632679489656, 0)),
                   Dual(6.12323399573676604e-17, -0))
    assert near_eq(cos(Dual(-1.57079632679489656, 0)),
                   Dual(6.12323399573676604e-17, 0))
    assert near_eq(cos(Dual(-0.785398163397448279, 0)),
                   Dual(0.707106781186547573, 0))
    assert near_eq(cos(Dual(0, 0)), Dual(1, -0))
    assert near_eq(cos(Dual(3.14159265358979312, 1)),
                   Dual(-1, -1.22464679914735321e-16))
    assert near_eq(cos(Dual(-3.14159265358979312, 1)),
                   Dual(-1, 1.22464679914735321e-16))
    assert near_eq(cos(Dual(1.57079632679489656, 1)),
                   Dual(6.12323399573676604e-17, -1))
    assert near_eq(cos(Dual(-1.57079632679489656, 1)),
                   Dual(6.12323399573676604e-17, 1))
    assert near_eq(cos(Dual(-0.785398163397448279, 1)),
                   Dual(0.707106781186547573, 0.707106781186547573))
    assert near_eq(cos(Dual(0, 1)), Dual(1, -0))
    assert near_eq(cos(Dual(3.14159265358979312, 0.100000000000000006)),
                   Dual(-1, -1.22464679914735327e-17))
    assert near_eq(cos(Dual(-3.14159265358979312, 0.100000000000000006)),
                   Dual(-1, 1.22464679914735327e-17))
    assert near_eq(cos(Dual(1.57079632679489656, 0.100000000000000006)), Dual(
        6.12323399573676604e-17, -0.100000000000000006))
    assert near_eq(cos(Dual(-1.57079632679489656, 0.100000000000000006)),
                   Dual(6.12323399573676604e-17, 0.100000000000000006))
    assert near_eq(cos(Dual(-0.785398163397448279, 0.100000000000000006)),
                   Dual(0.707106781186547573, 0.0707106781186547656))
    assert near_eq(cos(Dual(0.299999999999999989, 0.299999999999999989)), Dual(
        0.955336489125605981, -0.0886560619984018555))
    assert near_eq(cos(Dual(-0.299999999999999989, 0.299999999999999989)),
                   Dual(0.955336489125605981, 0.0886560619984018555))
    assert near_eq(cos(Dual(0.299999999999999989, -0.299999999999999989)),
                   Dual(0.955336489125605981, 0.0886560619984018555))
    assert near_eq(cos(Dual(-0.299999999999999989, -0.299999999999999989)),
                   Dual(0.955336489125605981, -0.0886560619984018555))
    assert near_eq(cos(Dual(0, 1)), Dual(1, -0))


def test_tan():
    assert near_eq(tan(Dual(3.14159265358979312, 0)),
                   Dual(-1.22464679914735321e-16, 0))
    assert near_eq(tan(Dual(-3.14159265358979312, 0)),
                   Dual(1.22464679914735321e-16, 0))
    assert near_eq(tan(Dual(1.57079632679489656, 0)),
                   Dual(16331239353195370, 0))
    assert near_eq(tan(Dual(-1.57079632679489656, 0)),
                   Dual(-16331239353195370, 0))
    assert near_eq(tan(Dual(-0.785398163397448279, 0)),
                   Dual(-0.999999999999999889, 0))
    assert near_eq(tan(Dual(0, 0)), Dual(0, 0))
    assert near_eq(tan(Dual(3.14159265358979312, 1)),
                   Dual(-1.22464679914735321e-16, 1))
    assert near_eq(tan(Dual(-3.14159265358979312, 1)),
                   Dual(1.22464679914735321e-16, 1))
    assert near_eq(tan(Dual(1.57079632679489656, 1)), Dual(
        16331239353195370, 2.66709378811357138e+32))
    assert near_eq(tan(Dual(-1.57079632679489656, 1)),
                   Dual(-16331239353195370, 2.66709378811357138e+32))
    assert near_eq(tan(Dual(-0.785398163397448279, 1)),
                   Dual(-0.999999999999999889, 1.99999999999999978))
    assert near_eq(tan(Dual(0, 1)), Dual(0, 1))
    assert near_eq(tan(Dual(3.14159265358979312, 0.100000000000000006)),
                   Dual(-1.22464679914735321e-16, 0.100000000000000006))
    assert near_eq(tan(Dual(-3.14159265358979312, 0.100000000000000006)),
                   Dual(1.22464679914735321e-16, 0.100000000000000006))
    assert near_eq(tan(Dual(1.57079632679489656, 0.100000000000000006)), Dual(
        16331239353195370, 2.66709378811357174e+31))
    assert near_eq(tan(Dual(-1.57079632679489656, 0.100000000000000006)),
                   Dual(-16331239353195370, 2.66709378811357174e+31))
    assert near_eq(tan(Dual(-0.785398163397448279, 0.100000000000000006)),
                   Dual(-0.999999999999999889, 0.199999999999999983))
    assert near_eq(tan(Dual(0.299999999999999989, 0.299999999999999989)), Dual(
        0.309336249609623248, 0.328706674596764115))
    assert near_eq(tan(Dual(-0.299999999999999989, 0.299999999999999989)),
                   Dual(-0.309336249609623248, 0.328706674596764115))
    assert near_eq(tan(Dual(0.299999999999999989, -0.299999999999999989)),
                   Dual(0.309336249609623248, -0.328706674596764115))
    assert near_eq(tan(Dual(-0.299999999999999989, -0.299999999999999989)),
                   Dual(-0.309336249609623248, -0.328706674596764115))
    assert near_eq(tan(Dual(0, 1)), Dual(0, 1))


def test_log():
    with pytest.raises((ValueError)):
        log(Dual(0, 0))
    assert near_eq(log(Dual(2.71828182845904509, 0)), Dual(1, 0))
    assert near_eq(log(Dual(5.43656365691809018, 0)),
                   Dual(1.69314718055994518, 0))
    with pytest.raises((ValueError)):
        log(Dual(-1.00000000000000002e-08, 0))
    with pytest.raises((ValueError)):
        log(Dual(0, 0))
    with pytest.raises((ValueError)):
        log(Dual(0, 1))
    with pytest.raises((ValueError)):
        log(Dual(0, -1))
    assert near_eq(log(Dual(1, 0)), Dual(0, 0))
    assert near_eq(log(Dual(1, 1)), Dual(0, 1))
    assert near_eq(log(Dual(1, -1)), Dual(0, -1))
    assert near_eq(log(Dual(10, 0)), Dual(2.3025850929940459, 0))
    assert near_eq(log(Dual(10, 1)), Dual(
        2.3025850929940459, 0.100000000000000006))
    assert near_eq(log(Dual(10, -1)),
                   Dual(2.3025850929940459, -0.100000000000000006))
    assert near_eq(log(Dual(10, 23)), Dual(
        2.3025850929940459, 2.30000000000000027))
    assert near_eq(log(Dual(10, -23)),
                   Dual(2.3025850929940459, -2.30000000000000027))


def test_exp():
    assert near_eq(exp(Dual(0, 0)), Dual(1, 0))
    assert near_eq(exp(Dual(0, 1)), Dual(1, 1))
    assert near_eq(exp(Dual(1, 1)), Dual(
        2.71828182845904509, 2.71828182845904509))
    assert near_eq(exp(Dual(1, 0.5)), Dual(
        2.71828182845904509, 1.35914091422952255))
    assert near_eq(exp(Dual(1, -0.5)),
                   Dual(2.71828182845904509, -1.35914091422952255))
    assert near_eq(exp(Dual(1, -1.5)),
                   Dual(2.71828182845904509, -4.07742274268856786))
    assert near_eq(exp(Dual(1, -1)),
                   Dual(2.71828182845904509, -2.71828182845904509))
    assert near_eq(exp(Dual(-1, 1)),
                   Dual(0.367879441171442334, 0.367879441171442334))
    assert near_eq(exp(Dual(-1, -1)),
                   Dual(0.367879441171442334, -0.367879441171442334))
    assert near_eq(exp(Dual(0, 12)), Dual(1, 12))
    assert near_eq(exp(Dual(12, 12)), Dual(
        162754.791419003916, 1953057.49702804699))
    assert near_eq(exp(Dual(12, 0.5)), Dual(
        162754.791419003916, 81377.3957095019578))
    assert near_eq(exp(Dual(12, -0.5)),
                   Dual(162754.791419003916, -81377.3957095019578))
    assert near_eq(exp(Dual(12, -12.5)),
                   Dual(162754.791419003916, -2034434.89273754903))
    assert near_eq(exp(Dual(12, -12)),
                   Dual(162754.791419003916, -1953057.49702804699))
    assert near_eq(exp(Dual(-12, 12)),
                   Dual(6.14421235332820981e-06, 7.37305482399385143e-05))
    assert near_eq(exp(Dual(-12, -12)),
                   Dual(6.14421235332820981e-06, -7.37305482399385143e-05))
    assert near_eq(exp(Dual(709.196208642166084, 0)),
                   Dual(1.00000000000001358e+308, 0))
    # overflow real part
    with pytest.raises((OverflowError)):
        exp(Dual(1000, 7))
        
    # overflow dual part
    with pytest.raises((OverflowError)):
        exp(Dual(709.196208642166084, 7))


def _test_functional():

    def f(x): return x
    assert f(Dual(3, 1)) == Dual(3, 1)

    def f(x): return x**2 + 3*x - 7
    def df(x): return 2*x + 3
    assert f(3) == 11
    assert f(3 + Dual(0, 1)) == Dual(3, 2)


if __name__ == "__main__":
    x = Dual(3, 1)
    y = Dual(4, 2)

    

    #print( x/ y)

    test_sqrt()
    test_mul()
    test_add()
    test_sub()
    test_divide()
    test_sin()
    test_log()
    test_exp()
    test_pow()

    x = Dual(709.196208642166084, 7)
    y = exp(x)
    
    test_mul()
    
    x = Dual(10,1)
    y = 3 * x*x
    print(x*x)
    def f(x): return x*x
    print(f(x))
    
    print(x*x*Dual(3,0))
    print(x*x*3)
    print(x*x*Dual(3,0))
    
    
