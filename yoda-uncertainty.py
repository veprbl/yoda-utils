#!/usr/bin/env python

import yoda
import numpy as np

def master_formula(get_value_func, num_members):
    val_0 = get_value_func(0)
    dys_p_sq = np.zeros(len(val_0.xs))
    dys_n_sq = np.zeros(len(val_0.xs))
    for member in range(1, num_members, 2):
        val_p = get_value_func(member)
        val_n = get_value_func(member + 1)
        assert (val_0.xs == val_p.xs).all()
        assert (val_0.xs == val_n.xs).all()
        dys_p_sq += np.max([val_p.ys - val_0.ys, val_n.ys - val_0.ys, np.zeros(len(val_0.ys))], 0) ** 2
        dys_n_sq += np.min([val_p.ys - val_0.ys, val_n.ys - val_0.ys, np.zeros(len(val_0.ys))], 0) ** 2
    val_0.dys_p = np.sqrt(dys_p_sq)
    val_0.dys_n = np.sqrt(dys_n_sq)
    return val_0

class XSec(object):
    pass

def read_xsec(filepath):
    y = yoda.read(filepath)
    h = y['/STAR_DIJET/d01-x01-y01']
    xsec = XSec()
    xsec.xs = np.array([x.xMid for x in h])
    xsec.xs_low = np.array([x.xMin for x in h])
    xsec.xs_high = np.array([x.xMax for x in h])
    xsec.ys = np.array([x.sumW for x in h]) / (xsec.xs_high - xsec.xs_low)
    return xsec

def get_xsec(member):
    filepath = "../CT10nlo_%02i.yoda" % member
    return read_xsec(filepath)

xsec = master_formula(get_xsec, 52)

s = yoda.Scatter2D("/STAR_DIJET/d01-x01-y01")
for (low, center, high, y, dp, dn) in zip(xsec.xs_low, xsec.xs, xsec.xs_high, xsec.ys, xsec.dys_p, xsec.dys_n):
    s.addPoint(center, y, xerrs=[center-low, high-center], yerrs=[dn, dp])

yoda.writeYODA([s], "pdf.yoda")
