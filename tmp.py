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
    return list

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
