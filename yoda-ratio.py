#!/usr/bin/env python2

import sys

import yoda


def find_point(scatter, x):
    for point in scatter:
        if point.x == x:
            return point
    raise IndexError("Matching point not found")

def div2d(s1, s2):
    s = yoda.Scatter2D()
    for p1 in s1:
        p2 = find_point(s2, p1.x)
        if p2.y != 0:
            s.addPoint(p1.x, p1.y / p2.y, xerrs = p1.xErrs)
        else:
            s.addPoint(p1.x, 0, xerrs = p1.xErrs)
    return s

if __name__ == '__main__':
    if (len(sys.argv) != 4):
        print "Usage: %s numerator denominator output" % sys.argv[0]
        sys.exit()

    numerator_filename = sys.argv[1]
    denominator_filename = sys.argv[2]
    output_filename = sys.argv[3]

    aos1 = yoda.readYODA(numerator_filename)
    aos2 = yoda.readYODA(denominator_filename)

    out_aos = []
    for ao in aos1.values():
        ao2 = aos2[ao.path]
        if isinstance(ao, yoda.core.Histo1D):
            assert isinstance(ao2, yoda.core.Histo1D)
            r = ao / ao2
        elif isinstance(ao, yoda.core.Scatter2D):
            r = div2d(ao, ao2)
        else:
            continue
        r.path = ao.path
        r.setAnnotation("LogY", 0)
        out_aos.append(r)
    yoda.writeYODA(out_aos, output_filename)
