#!/usr/bin/python

import vertex_list
import svg
import sys
from optparse import OptionParser

def main():
    parser = OptionParser(usage="usage: %prog [options] inputfile")
    parser.add_option("-o", dest="output", type="string",
                      help="output file", metavar="FILE")
    parser.add_option("-u", dest="unit_tests", action="store_true",
                      help="run unit tests")
    parser.add_option("-t", dest="tests", action="store_true",
                      help="run tests")
    (options, args) = parser.parse_args()

    if options.unit_tests:
        run_unit_tests()
        return

    if options.tests:
        run_tests()
        return

    if len(args) != 1:
        parser.print_help()
        return

    vertices = vertex_list.VertexList(args[0])
    svg_out = svg.SVG(options.output)
    for vertex in vertices:
        svg_out.draw_vertex(vertex)
    svg_out.draw_hull(vertices.convex_hull())
    svg_out.flush()

if __name__ == "__main__":
    main()
