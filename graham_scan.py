import vertex_list
import svg

if __name__ == "__main__":
    list = vertex_list.VertexList('input')
    svg = svg.SVG('test.svg')
    for p in list:
        svg.draw_vertex(p)
    svg.draw_hull(list.convex_hull())
    svg.flush()
