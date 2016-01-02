#!/usr/bin/env python2

"""
Converts yoda Histo1D to Scatter2D (ignoring stat. uncertainty)
"""

import sys

import yoda

def process(item):
    if isinstance(item, yoda.core.Histo1D):
        s = yoda.Scatter2D(item.path)
        for hbin in item:
            s.addPoint(hbin.xMid, hbin.height, xerrs=[hbin.xWidth/2, hbin.xWidth/2])
        return s
    elif isinstance(item, yoda.core.Scatter2D):
        for point in item:
            point.yErrs=(0,0)
	return item
    return item

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print "Usage: %s input output" % sys.argv[0]
        sys.exit()

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    y = yoda.readYODA(input_filename)
    y = map(process, y.values())
    yoda.writeYODA(y, output_filename)
