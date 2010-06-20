from my_list import MyList

class VertexList():

    """A list of (x, y) vertices representing a vertex set.
    
    Provides a specialized methods for Graham scan implementation.

    Instance variables:
        x_min
        x_max
        y_min
        y_max
        lowest_y -- vertex with the lowest y coordinate
        list -- the actual list
        length -- length of the list
        fst_free -- first free index

    Methods:
        append(element)
        graham_sort()
        convex_hull()

    Initialization:
        If a filename is given, parse vertices from file.

        Exceptions:
            IOError
            ValueError

    """
    def __init__(self, filename=None, size=100, fst_free=0):
        self.list = list(size*' ')
        self.length = size
        self.fst_free = fst_free
        self.__iter_spot = 0
        self.x_min = float('inf')
        self.x_max = float('-inf')
        self.y_min = float('inf')
        self.y_max = float('-inf')
        self.lowest_y = (float('inf'), float('inf'))
        if filename is not None:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.split(' ')
                    x = float(line[0])
                    y = float(line[1])
                    self.append((x, y))

    def append(self, vertex):
        """Append a vertex to list and update min and max info.
        
        Arguments:
            vertex -- (x, y) vertex in R^2
        
        """
        if vertex[0] < self.x_min:
            self.x_min = vertex[0]
        if vertex[0] > self.x_max:
            self.x_max = vertex[0]

        if vertex[1] < self.y_min or \
           (vertex[1] == self.y_min and \
            vertex[0] < self.lowest_y[0]):
            self.y_min = vertex[1]
            self.lowest_y = vertex
        if vertex[1] > self.y_max:
            self.y_max = vertex[1]

        self.list[self.fst_free] = vertex
        self.fst_free += 1
        if self.fst_free == self.length:
            self.__grow()

    def __grow(self):
        """Double the size of the list"""
        old = list(self.list)
        self.list = list(self.length*2*' ')
        self.length = self.length*2
        for i in range(0, len(old)):
            self.list[i] = old[i]

    def __getitem__(self, i):
        """Return listitem in index i, or raise IndexError."""
        if i < self.fst_free:
            return self.list[i]
        raise IndexError("list index out of range")

    def __getslice__(self, s, e):
        """Return a slice from s to e."""
        return self.list[s:e]

    def __setitem__(self, i, e):
        """Set list item in index i to e."""
        if i >= self.fst_free:
            raise IndexError("list index out of range")
        self.list[i] = e

    def __len__(self):
        """Return the length of the list."""
        return self.fst_free

    def __iter__(self):
        """Return a iterator of the list."""
        return self

    def next(self):
        """Return the next element in iteration, or raise StopIteration.

        Only actual elements (added with append()) are iterated over.

        """
        if self.__iter_spot >= self.fst_free:
            raise StopIteration()
        else:
            self.__iter_spot += 1
            return self.list[self.__iter_spot-1]

    def index(self, x):
        """Return smallest i such that self[i] == x"""
        for i in range(0, len(self)):
            if self[i] == x:
                return i
        raise ValueError('%s not in list'%(x))

    def __cmp_value(self, x):
        """Return the contangent of the angle between the x-axis and a line via
        x and the vertex with the lowest y coordinate.

        Arguments:
            x -- a vertex in R^2

        Exceptions:
            TypeError

        """
        try:
            return float(self.lowest_y[0] - x[0]) / float(self.lowest_y[1] - x[1])
        except ZeroDivisionError:
            if x[0] > self.lowest_y[0] or x == self.lowest_y:
                return float('inf')
            else:
                return float('-inf')

    def __cmp_function(self, x, y):
        """Compare x to y.

        Primary comparison is done based on the polar angle of the vertex. Secondary
        comparison is done based on the x coordinates.

        Arguments:
            x -- a vertex in R^2
            y -- a vertex in R^2

        Exceptions:
            TypeError

        Returns:
            Negative, zero or positive value depending whether x is smaller,
            equal or greater than y.

        """
        x_polar = self.__cmp_value(x)
        y_polar = self.__cmp_value(y)

        if x_polar < y_polar:
            return 1
        elif x_polar > y_polar:
            return -1
        elif x[0] < y[0]:
            return -1
        elif x[0] > y[0]:
            return 1
        else:
            return 0

    def graham_sort(self):
        """Sort vertices to increasing order.

        Vertices are sort based on the angle between the x-axis and a line via
        the vertex with the lowest y coordinate and the vertex itself.

        """
        i = self.index(self.lowest_y)
        self[0], self[i] = self[i], self[0]
        # list.sort(self, cmp=self.__cmp_function)
        self.__quicksort(0, len(self)-1)

    def convex_hull(self):
        """Calculate the convex hull of the vertex set.

        Convex hull is calculated using the Graham scan algorithm.
        Innerfunction ccw is used to determine whether theree vertices make a
        left or a right turn.

        Exceptions:
            TypeError

        Returns:
            A list of vertecies that represen the convex hull of the vertex
            set.
            
        """
        def ccw(p1, p2, p3):
            return (p2[0] - p1[0])*(p3[1] - p1[1]) - (p2[1] - p1[1])*(p3[0] - p1[0]) <= 0

        if len(self) <= 3:
            return self

        self.graham_sort()
        m = 1
        for i in range(2, len(self)):
            while m > 0 and ccw(self[m-1], self[m], self[i]):
                m -= 1
            m += 1
            self[m], self[i] = self[i], self[m]
        return self[:m+1]

    def __quicksort(self, left, right):
        """Sort self with non-stable quicksort between indices left and right.

        cmp_function is used to compare two elements. When array length is
        shorten than 20, insertion sort is used to finish the sort.

        Arguments:
            left -- first index
            right -- last index

        Exceptions:
            TypeError
            IndexError

        """
        if right > left:
            split = self.__partition(left, right, (left+right)/2)
            self.__quicksort(left, split-1)
            self.__quicksort(split+1, right)

    def __partition(self, left, right, pivot):
        """Partition self around pivot between left and right.
        
        A helper function for __quicksort().
        
        Returns:
            The new index of the pivot value.
            
        """
        self[pivot], self[right] = self[right], self[pivot]
        split = left
        for i in range(left, right):
            if self.__cmp_function(self[i], self[right]) <= 0:
                self[i], self[split] = self[split], self[i]
                split += 1
        self[split], self[right] = self[right], self[split]
        return split

