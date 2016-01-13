#!/usr/bin/env python

import argparse

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
    def __init__(self, ao):
        self.xs = np.array([x.xMid for x in ao])
        self.xs_low = np.array([x.xMin for x in ao])
        self.xs_high = np.array([x.xMax for x in ao])
        self.ys = np.array([x.height for x in ao])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=True, help="Path to the output file")
    parser.add_argument("-c", "--central", required=True, help="Central values input file")
    parser.add_argument("-t", "--type", required=True, choices=["hessian"], help="PDF error vectors type")
    parser.add_argument("other", nargs='*', help="Other input files")
    args = parser.parse_args()

    central_aos = yoda.read(args.central)
    output_aos = []
    for ao in central_aos.values():
        if not isinstance(ao, yoda.core.Histo1D):
            continue
        print ao.path
        num_members = len(args.other)
        def get_xsec(member):
            if member == 0:
                return XSec(ao)
            y = yoda.read(args.other[member-1])
            member_ao = y[ao.path]
            return XSec(member_ao)
        xsec = master_formula(get_xsec, num_members)
        s = yoda.Scatter2D(ao.path)
        for (low, center, high, y, dp, dn) in zip(xsec.xs_low, xsec.xs, xsec.xs_high, xsec.ys, xsec.dys_p, xsec.dys_n):
            s.addPoint(center, y, xerrs=[center-low, high-center], yerrs=[dn, dp])
        output_aos.append(s)

    yoda.writeYODA(output_aos, args.output)
