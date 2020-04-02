#!/usr/bin/env python

import numpy as np
from numbers import Number

def parallel(z1, z2, *args):

    reciprocal_sum = 1/z1 + 1/z2

    for arg in list(args):
        reciprocal_sum += 1/arg

    return 1/reciprocal_sum

def magnitude(c):
    if isinstance(c, Number):
        complex_num = complex(c)
    else:
        complex_num = c.astype(complex)

    return np.sqrt(complex_num.real**2 + complex_num.imag**2)

def phase(c):
    if isinstance(c, Number):
        complex_num = complex(c)
    else:
        complex_num = c.astype(complex)

    return np.arctan2(complex_num.imag, complex_num.real)