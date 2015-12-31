#!/usr/bin/env python2

import sys

import yoda



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
        if not isinstance(ao, yoda.core.Histo1D):
            continue
        ao2 = aos2[ao.path]
	r = ao / ao2
	r.path = ao.path
	r.setAnnotation("LogY", 0)
	print dir(r)
	out_aos.append(r)
    yoda.writeYODA(out_aos, output_filename)
