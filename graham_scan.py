import vertex_list
import svg

if __name__ == "__main__":
    list = vertex_list.VertexList('input')
    print list
    list.graham_sort()
    print list
