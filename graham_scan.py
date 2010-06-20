#!/usr/bin/python

import vertex_list
import svg
import sys
from random import randint, seed
from optparse import OptionParser

def draw(input, output):
    """Draw vertices and convex hull from 'input' to 'output'."""
    vertices = vertex_list.VertexList(input)
    svg_out = svg.SVG(output)
    for vertex in vertices:
        svg_out.draw_vertex(vertex)
    svg_out.draw_hull(vertices.convex_hull())
    svg_out.flush()

def run_tests():
    # static random seed
    seed(1)

    quarters = [vertex_list.VertexList(),
                vertex_list.VertexList(),
                vertex_list.VertexList(),
                vertex_list.VertexList()]
    # first quarter of Cartesian plane
    for x in range(0, 11):
        for y in range(0, 11):
            quarters[0].append((randint(0, 100), randint(0, 100)))
    # second quarter
    for x in range(0, 11):
        for y in range(0, 11):
            quarters[1].append((randint(0, 100), -randint(0, 100)))
    # third quarter
    for x in range(0, 11):
        for y in range(0, 11):
            quarters[2].append((-randint(0, 100), -randint(0, 100)))
    # fourth quarter
    for x in range(0, 11):
        for y in range(0, 11):
            quarters[3].append((-randint(0, 100), randint(0, 100)))

    for i in range(0, 4):
        draw(quarters[i], '%squarter.svg'%(i+1))

    all_over_the_place = vertex_list.VertexList()
    for x in range(0, 11):
        for y in range(0, 11):
            all_over_the_place.append((((-1)**x)*randint(0, 100),
                                      ((-1)**y)*randint(0, 100)))
    draw(all_over_the_place, 'everywhere.svg')

def main():
    """The main method.

    Parse command line flags, and either run the tests or calculate and
    visualize the convex hull from the 'inputfile'.

    """
    parser = OptionParser(usage="usage: %prog [options] inputfile")
    parser.add_option("-o", dest="output", type="string",
                      help="output file", metavar="FILE")
    parser.add_option("-t", dest="tests", action="store_true",
                      help="run tests")
    (options, args) = parser.parse_args()

    if options.tests:
        run_tests()
        return

    if len(args) != 1:
        parser.print_help()
        return

    draw(args[0], options.output)

if __name__ == "__main__":
    main()
