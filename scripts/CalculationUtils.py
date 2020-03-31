#!/usr/bin/env python

import numpy as np
from numbers import Number

def parallel(z1, z2, *args):
    for arg in args:
        if not isinstance(arg, Number):
            raise TypeError("tried to perform parallel impedance calculation with non-numbers")
    
    reciprocal_sum = 1/z1 + 1/z2

    for arg in args:
        reciprocal_sum = 1/arg

    return 1/reciprocal_sum

def magnitude(c):
    complex_num = c.astype(complex)

    return np.sqrt(complex_num.real**2 + complex_num.imag**2)

def phase(c):
    complex_num = c.astype(complex)

    return np.arctan2(complex_num.imag, complex_num.real)