import numpy
import timeit


def line(x0, y0, x1, y1, matrix):
    sum   = 0
    dx    = abs(x1-x0)
    sx    = 1 if x0 < x1 else -1
    dy    = -abs(y1-y0)
    sy    = 1 if y0 < y1 else -1
    err   = dx+dy  # error value e_xy

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


def calc_target(x, y, size):
    if x < size/2 and y < size/2:
        return size, size
    elif x >= size/2 > y:
        return 0, size
    elif x < size/2 <= y:
        return size, 0
    else:
        return 0, 0


def bresenham_test(steps, size, matrix):
    array = []
    for y in range(0, 1, steps):
        for x in range(0, size, steps):
            target = calc_target(x, y, size)
            sum = line(x, y, target[0], target[1], matrix)
            #sum = x*y
            array.append(sum)
    return array


def run_test():
    # variables
    height_map_size = 2048
    steps = 1  # Determines how many pixels will be skipped

    # data structures
    matrix = numpy.random.rand(height_map_size, height_map_size)

    # test
    start = timeit.default_timer()
    array = bresenham_test(steps, height_map_size, matrix)
    stop = timeit.default_timer()

    # output
    print("Time: " + str(round(stop - start, 2)) + "s")
    # print(array)
