#!/usr/bin/env python2

import argparse

import yoda

def find_point(scatter, x):
    for point in scatter:
        if point.x == x:
            return point
    raise IndexError("Matching point not found")

def envelope(central, others):
    s = yoda.Scatter2D(central.path)
    if isinstance(central, yoda.core.Histo1D):
        for hbin in central:
            x = hbin.xMid
            y = hbin.height
            max_y = y
            min_y = y
            for other in others:
                assert isinstance(other, yoda.core.Histo1D)
                other_bin = other.binAt(x)
                max_y = max(max_y, other_bin.height)
                min_y = min(min_y, other_bin.height)
            s.addPoint(x, y, xerrs=[hbin.xWidth/2, hbin.xWidth/2], yerrs=[y - min_y, max_y - y])
    elif isinstance(central, yoda.core.Scatter2D):
        for point in central:
            max_y = point.y
            min_y = point.y
            for other in others:
                assert isinstance(other, yoda.core.Scatter2D)
                other_point = find_point(other, point.x)
                max_y = max(max_y, other_point.y)
                min_y = min(min_y, other_point.y)
            s.addPoint(point.x, point.y, xerrs=point.xErrs, yerrs=[point.y - min_y, max_y - point.y])
    else:
        return None
    return s

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=True, help="Path to the output file")
    parser.add_argument("-c", "--central", required=True, help="Central values input file")
    parser.add_argument("other", nargs='*', help="Other input files")
    args = parser.parse_args()

    central = yoda.readYODA(args.central)
    other = map(yoda.readYODA, args.other)

    output_aos = []
    for central_ao in central.values():
        other_aos = [other_ao[central_ao.path] for other_ao in other]
        envelope_ao = envelope(central_ao, other_aos)
        if envelope_ao is not None:
            output_aos.append(envelope_ao)
    yoda.write(output_aos, args.output)
