import vertex_list
import svg
import sys

if __name__ == "__main__":
    list = vertex_list.VertexList(sys.argv[1])
    svg = svg.SVG('test.svg')
    for p in list:
        svg.draw_vertex(p)
    svg.draw_hull(list.convex_hull())
    svg.flush()
