def parse_file(filepath):
    """Parse points from the file into a list.

    Arguments:
    filepath -- a string containing a path to the input file

    Exceptions:
    IOError
    ValueError

    Returns:
    A list of (x, y) tuples.

    """
    list = []
    file = open(filepath)
    for line in file:
        x = float(line.split(' ')[0])
        y = float(line.split(' ')[1])
        list.append((x, y))
    file.close()
    return list

def visualize(points, filepath, hull=[]):
    def x_min_max(points):
        min = float('inf')
        max = float('-inf')
        for p in points:
            if p[0] < min:
                min = p[0]
            if p[0] > max:
                max = p[0]
        return (min, max)

    def y_min_max(points):
        min = float('inf')
        max = float('-inf')
        for p in points:
            if p[1] < min:
                min = p[1]
            if p[1] > max:
                max = p[1]
        return (min, max)

    x_min = x_min_max(points)[0]
    x_max = x_min_max(points)[1]
    y_min = y_min_max(points)[0]
    y_max = y_min_max(points)[1]

    svg_points = to_svg_points(points, x_min, y_max)

    f = open(filepath, 'a')
    svg_pre(x_max - x_min, y_max - y_min, f)
    draw_axes(x_min, x_max, y_min, y_max, f)
    draw_points(svg_points, f)
    if len(hull) > 0:
        draw_hull(to_svg_points(hull, x_min, y_max), f)
    svg_suf(f)
    f.close()

def svg_pre(width, height, f):
    f.write("<?xml version=\"1.0\" standalone=\"no\"?>\n")
    f.write("<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n")
    f.write("\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n")
    f.write("<svg width=\"100%s\" height=\"100%s\" viewBox=\"0 0 %s %s\" version=\"1.1\" \n" \
            %('%', '%', width + 10, height + 10))
    f.write("xmlns=\"http://www.w3.org/2000/svg\">\n")

def svg_suf(f):
    f.write("</svg>")

def to_svg_points(points, x_min, y_max):
    svg_points = []
    for p in points:
        svg_points.append((p[0] - x_min, y_max - p[1]))
    return svg_points

def draw_line(start, end, f):
    f.write("<line x1=\"%s\" y1=\"%s\" x2=\"%s\" y2=\"%s\" stroke=\"black\" stroke-width=\"1\"/>\n"\
            %(start[0], start[1], end[0], end[1]))

def draw_axes(x_min, x_max, y_min, y_max, f):
    if x_min > 0:
        x_min = 0
    if y_min > 0:
        y_min = 0
    x_min = abs(x_min)
    # x-axis
    f.write("<line x1=\"%s\" y1=\"%s\" x2=\"%s\" y2=\"%s\" stroke=\"black\" stroke-width=\"1\"/>\n"\
            %(0, y_max,2*x_max, y_max))
    # y-axis
    f.write("<line x1=\"%s\" y1=\"%s\" x2=\"%s\" y2=\"%s\" stroke=\"black\" stroke-width=\"1\"/>\n"\
            %(x_min, 0, x_min, y_max - y_min))

def draw_points(svg_points, f):
    for p in svg_points:
        f.write("<circle cx=\"%s\" cy=\"%s\" r=\"0.5\" stroke=\"black\" \
                stroke-width=\"0.01\" fill=\"black\"/>\n"%(p[0], p[1]))

def draw_hull(hull, f):
    for i in range(0, len(hull)):
        if i+1 < len(hull):
            draw_line(hull[i], hull[i+1], f)
        else:
            draw_line(hull[i], hull[0], f)

def make_get_cmp_value(p):
    """Return a function that takes x and calls f(p, x).

    >>> make_get_cmp_value((1, 1))((2, 1))
    inf
    >>> make_get_cmp_value((1, 1))((2, 2))
    1.0
    >>> make_get_cmp_value((1, 1))((1, 2))
    -0.0
    >>> make_get_cmp_value((1, 1))((0, 2))
    -1.0
    >>> make_get_cmp_value((1, 1))((0, 1))
    -inf
    """
    def f(p, x):
        """Return the cotangent of the angle between the x-axis and a line via
        p and x.

        Arguments:
        p -- an point (x, y) in R^2
        x -- an point (x, y) in R^2

        Exceptions:
        TypeError

        """
        try:
            return float(p[0]-x[0]) / float(p[1]-x[1])
        except ZeroDivisionError:
            if x[0] > p[0] or x == p:
                return float('inf')
            else:
                return float('-inf')
    return lambda x: f(p, x)

def graham_scan(points):
    """Take a list of (x, y) points and return points defining a convext hull.

    Arguments:
    points -- a list of (x, y) points in R^2

    Exceptions:
    TypeError

    Returns:
    A list of points defining the convext hull.

    """
    def index_of_lowest_y(points):
        lowest = 0
        for i in range(1, len(points)):
            if points[i][1] < points[lowest][1] or \
               (points[i][1] == points[lowest][1] and \
                points[i][0] < points[lowest][0]):
                lowest = i
        return lowest

    def is_ccw(p1, p2, p3):
        return (p2[0] - p1[0])*(p3[1] - p1[1]) - (p2[1] - p1[1])*(p3[0] - p1[0]) <= 0

    i = index_of_lowest_y(points)
    print points[i]
    points[1], points[i] = points[i], points[1]
    points.sort(key=make_get_cmp_value(points[1]), reverse=True)

    m = 1
    for i in range(2, len(points)):
        while is_ccw(points[m-1], points[m], points[i]) and m > 0:
            m -= 1
        m += 1
        points[m], points[i] = points[i], points[m]

    return points[:m+1]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print graham_scan(parse_file('input'))
