import os
import vertex_list

class SVG:
    """SVG image representation of 2D vertices and lines. Vertex and line data
    is kept in memory until writen to file with the flush() method.

    Instance variables:
        filename -- path to not existing file
        lines -- a VertexList of (x1, y1, x2, y2) vertex pairs
        vertices -- a list of (x, y) vertices

    Methods:
        draw_vertex()
        draw_line()
        draw_hull()
        flush()

    Init:
        If given filename already exist, IOError is raised. Otherwise 'lines' and
        'vertices' lists are initialized.

    """
    def __init__(self, filename):
        if os.path.exists(filename):
            raise IOError("file %s already exists"%(filename))
        self.filename = filename
        self.lines = []
        self.vertices = vertex_list.VertexList()

    def __write_prelude(self, file):
        """Write SVG prelude info to file"""
        width = self.vertices.x_max - self.vertices.x_min
        if self.vertices.x_max < 0:
            width = abs(self.vertices.x_min)
        if self.vertices.x_min > 0:
            width = self.vertices.x_max

        height = self.vertices.y_max - self.vertices.y_min
        if self.vertices.y_max < 0:
            height = abs(self.vertices.y_min)
        if self.vertices.y_min > 0:
            height = self.vertices.y_max

        file.write('<?xml version="1.0" standalone="no"?>\n')
        file.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n')
        file.write('"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
        file.write('<svg width="100%s" height="100%s" viewBox="0 0 %s %s" version="1.1"\n'\
            %('%', '%', width + 10, height + 10))
        file.write('xmlns="http://www.w3.org/2000/svg">\n')

    def draw_vertex(self, vertex):
        """Add vertex (x, y) to 'vertices' to be writen when flushed."""
        self.vertices.append(vertex)

    def draw_line(self, x1, y1, x2, y2):
        """Add line (x1, y1, x2, y2) to 'lines' to be writen when flushed."""
        self.lines.append((x1, y1, x2, y2))

    def draw_hull(self, vertices):
        """Add appropriate lines to outline the hull."""
        for i in range(0, len(vertices)):
            if i+1 < len(vertices):
                self.draw_line(vertices[i][0], vertices[i][1],
                               vertices[i+1][0], vertices[i+1][1])
            else:
                self.draw_line(vertices[i][0], vertices[i][1],
                               vertices[0][0], vertices[0][1])

    def __draw_axes(self, file):
        """Draw appropriate lines to draw x and y-axes."""
        x_min = self.vertices.x_min
        if x_min > 0:
            x_min = 0
        y_min = self.vertices.y_min
        if y_min > 0:
            y_min = 0
        # x-axis
        self.draw_line(x_min, 0, self.vertices.x_max, 0)
        # y-axis
        self.draw_line(0, self.vertices.y_max, 0, y_min)

        #width = self.vertices.x_max - self.vertices.x_min
        #if self.vertices.x_max < 0:
        #    width = abs(self.vertices.x_min)
        #if self.vertices.x_min > 0:
        #    width = self.vertices.x_max

        #height = self.vertices.y_max - self.vertices.y_min
        #if self.vertices.y_max < 0:
        #    height = abs(self.vertices.y_min)
        #if self.vertices.y_min > 0:
        #    height = self.vertices.y_max
        ## x-axis
        #file.write('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="black" stroke-width="0.05"/>\n'\
        #            %(0, height/2, width, height/2))
        ## y-axis
        #file.write('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="black" stroke-width="0.05"/>\n'\
        #            %(width/2, 0, width/2, height))

    def __to_svg_vertex(self, vertex):
        return (vertex[0] - self.vertices.x_min,
                self.vertices.y_max - vertex[1] + 5)

    def flush(self):
        """Open 'filename' and write current vertecies and lines to it.

        Exceptions:
            IOError
            ValueError

        """
        with open(self.filename, 'w') as file:
            self.__write_prelude(file)
            self.__draw_axes(file)
            for v in self.vertices:
                svg_v = self.__to_svg_vertex(v)
                file.write('<circle cx="%s" cy="%s" r="0.05" stroke="black"\
 stroke-width="0.05" fill="black" />\n'%(svg_v[0], svg_v[1]))
            for l in self.lines:
                svg_from = self.__to_svg_vertex((l[0], l[1]))
                svg_to = self.__to_svg_vertex((l[2], l[3]))
                file.write('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="black" stroke-width="0.05"/>\n'\
                                %(svg_from[0], svg_from[1], svg_to[0], svg_to[1]))
            file.write('</svg>\n')

