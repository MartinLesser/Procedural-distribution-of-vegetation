cimport numpy
import numpy
import timeit

cdef double line(int x0, int y0, int x1, int y1, numpy.ndarray matrix):
    cdef double sum     = 0
    cdef int dx         = abs(x1-x0)
    cdef int sx         = 1 if x0 < x1 else -1
    cdef int dy         = -abs(y1-y0)
    cdef int sy         = 1 if y0 < y1 else -1
    cdef int err        = dx+dy  # error value e_xy

    while True:
        if x0 == x1 and y0 == y1:
            return sum
        else:
            sum += matrix[x0, y0]
        e2 = 2*err
        if e2 > dy:
            err += dy
            x0 += sx  # e_xy+e_x > 0
        if e2 < dx:
            err += dx
            y0 += sy  # e_xy+e_y < 0


cdef list calc_target(int x, int y, int size):
    cdef list result = []
    if x < size/2 and y < size/2:
        result.append(size)
        result.append(size)
    elif x >= size/2 > y:
        result.append(0)
        result.append(size)
    elif x < size/2 <= y:
        result.append(size)
        result.append(0)
    else:
        result.append(0)
        result.append(0)
    return result


cdef list bresenham_test(int steps, int size, numpy.ndarray matrix):
    cdef list array = [], target = []
    cdef int x, y
    cdef double sum = 0
    for y in range(0, size, steps):
        for x in range(0, size, steps):
            target = calc_target(x, y, size)
            sum = line(x, y, target[0], target[1], matrix)
            array.append(sum)
    return array

def run_test():
    # variables
    cdef int height_map_size = 8192
    cdef int steps = 100  # Determines how many pixels will be skipped

    # data structures
    cdef numpy.ndarray matrix = numpy.random.rand(height_map_size, height_map_size)

    # test
    cdef int start = timeit.default_timer()
    cdef list array = bresenham_test(steps, height_map_size, matrix)
    cdef int stop = timeit.default_timer()

    # output
    print("Time: " + str(round(stop - start, 2)) + "s")
    #print(array)