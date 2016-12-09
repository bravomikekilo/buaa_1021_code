# -*- coding: utf-8 -*-
import config
import math as m


def solve(a, b, c):
    """solve the equation and take the bigger root"""
    return (-b + m.sqrt(b * b - 4 * a * c)) / (2. * a)


def get_result(rt):
    """get the temperature from the resistance using the config parameters"""
    return solve(config.B * config.R0, config.A * config.R0, config.R0 - rt)


def find_the_peak(x):
    """find the change point of the temperature. Raise ValueError if cannot find them"""
    diff = map(lambda y: y[0] - y[1], zip(x[1:], x))
    for i in range(1, len(diff)):
        print diff[i]
        if abs(diff[i]) > abs(5 * diff[i - 1]):
            first = i
            break

    for i in range(1, len(diff)):
        if diff[i] > 0:
            secd = i
            break
    try:
        return first+1, secd+1
    except NameError, _:
        raise ValueError('wrong data, cannot infer the data section')


def section_data(x):
    """section the data using the change point of the temperature"""
    f, s = find_the_peak(x[:, 0])
    return x[:f], x[f - 1: s], x[s:]
