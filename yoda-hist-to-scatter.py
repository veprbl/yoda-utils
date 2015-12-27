#!/usr/bin/env python2

"""
Converts yoda Histo1D to Scatter2D (ignoring stat. uncertainty)
"""

import sys

import yoda

def process(item):
    if not isinstance(item, yoda.core.Histo1D):
        return item
    hist = item
    s = yoda.Scatter2D(item.path)
    for hbin in hist:
        s.addPoint(hbin.xMid, hbin.height, xerrs=[hbin.xWidth/2, hbin.xWidth/2])
    print s
    return s

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print "Usage: %s input output" % sys.argv[0]

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    y = yoda.readYODA(input_filename)
    print y
    y = map(process, y.values())
    yoda.writeYODA(y, output_filename)
