import math
import numpy as np


class Orography:
    """
    The orography class calculates the normal map based on the height map.
    """
    @staticmethod
    def calculate_normal(vector1, vector2, vector3):
        """
        Calculates the normal vector from three vertices. First two direction vectors will be calculated and
        via cross product the normal vector will be calculated.
        :param vector1, vector2, vector3: three vertices.
        :return: Cross product of the calculated direction vectors.
        """
        vector_a = [a_i - b_i for a_i, b_i in zip(vector2, vector1)]
        vector_b = [a_i - b_i for a_i, b_i in zip(vector3, vector1)]
        return np.cross(vector_a, vector_b).tolist()

    @staticmethod
    def normalize(raw):
        """
        Normalizes a vector by squaring each component and adding the results. The square root of the sum will
        be calculted. The result is used to divide each vector component. This normalizes the vector.
        :param raw: Unnormalized vector.
        :return: Normalized vector.
        """
        sum = 0
        for v in raw:
            sum += v ** 2
        length = math.sqrt(sum)
        return [float(i) / length for i in raw]

    @staticmethod
    def add_vectors(vector1, vector2):
        return [a_i + b_i for a_i, b_i in zip(vector1, vector2)]

    @staticmethod
    def create_vertex_list(map, image_height_map):
        """
        Creates a vertex list. This uses the height map. Each pixel will be transformed to a vertex. The x- and y-position
        will be determined by the pixel position multiplied with the pixel size to receive the real position. The z-position
        is determined by the height value multiplied with height conversion value. Furthermore the list will get a
        padding by repeating the edge vertices. This is necessary for calculating the normals, which need the neighbours.
        :param map: Object of the map class. Used for the pixel size and the height conversion value.
        :param image_height_map: Image of the height map.
        :return: vertex_list: List of the determined vertices.
        """
        vertex_list = []
        row = [[0, 0, image_height_map.image[0][0] * map.height_conversion]]
        for x in range(1, image_height_map.size + 1):
            row.append([map.pixel_size * x, 0, image_height_map.image[0][x - 1] * map.height_conversion])
        row.append([(image_height_map.size + 1) * map.pixel_size, 0,
                    image_height_map.image[0][image_height_map.size - 1] * map.height_conversion])
        vertex_list.append(row)
        for y in range(1, image_height_map.size + 1):
            row = [[0, y * map.pixel_size, image_height_map.image[y - 1][0] * map.height_conversion]]
            for x in range(1, image_height_map.size + 1):
                row.append(
                    [x * map.pixel_size, y * map.pixel_size,
                     image_height_map.image[y - 1][x - 1] * map.height_conversion])
            row.append(
                [(image_height_map.size + 1) * map.pixel_size,
                 y * map.pixel_size,
                 image_height_map.image[y - 1][image_height_map.size - 1] * map.height_conversion])
            vertex_list.append(row)
        row = [[0, (image_height_map.size + 1) * map.pixel_size,
                image_height_map.image[image_height_map.size - 1][image_height_map.size - 1] * map.height_conversion]]
        for x in range(1, image_height_map.size + 1):
            row.append([x * map.pixel_size,
                        (image_height_map.size + 1) * map.pixel_size,
                        image_height_map.image[image_height_map.size - 1][x - 1] * map.height_conversion])
        row.append([(image_height_map.size + 1) * map.pixel_size,
                    (image_height_map.size + 1) * map.pixel_size,
                    image_height_map.image[image_height_map.size - 1][image_height_map.size - 1] * map.height_conversion])
        vertex_list.append(row)
        return vertex_list

    @staticmethod
    def calculate_normal_map(map, image_height_map):
        """
        Calculates all normal vector of a map. It needs the previously calculated vertex list. For calculating the
        normal of a vertex all neighbour normal will be calculated, added up and normalized. Each vertex has six
        neighbour faces, which have a normal vector. These normals have to be calculated. The calculation is done by
        determining the direction vectors of three vertices (the oberserved vertex + 2 neighbour vertices). The
        cross product of the two directions vectors will be calculated resulting in the normal of that surface.
        :param map: Object of the map class. Used for creating the vertex list.
        :param image_height_map: Image of the height map. Used for creating the vertex list.
        :return: normals: List of all calculated normals of each pixel.
        """
        vertex_list = Orography.create_vertex_list(map, image_height_map)
        array_size = len(vertex_list[0]) - 2
        padded_array = vertex_list
        normals = []
        for y in range(1, array_size + 1):
            print("Calculating normal map. Row: " + str(y))
            row = []
            for x in range(1, array_size + 1):
                # print("Calculating normal map. Column: " + str(x))
                sum = [0.0, 0.0, 0.0]
                # first neighbour triangle
                triangle_normal = Orography.calculate_normal(padded_array[y][x],
                                                             padded_array[y][x - 1],
                                                             padded_array[y - 1][x - 1],
                                                             )
                sum = Orography.add_vectors(sum, triangle_normal)
                # second neighbour triangle
                triangle_normal = Orography.calculate_normal(padded_array[y][x],
                                                             padded_array[y - 1][x - 1],
                                                             padded_array[y - 1][x],
                                                             )
                sum = Orography.add_vectors(sum, triangle_normal)
                # third neighbour triangle
                triangle_normal = Orography.calculate_normal(padded_array[y][x],
                                                             padded_array[y - 1][x],
                                                             padded_array[y][x + 1],
                                                             )
                sum = Orography.add_vectors(sum, triangle_normal)
                # fourth neighbour triangle
                triangle_normal = Orography.calculate_normal(padded_array[y][x],
                                                             padded_array[y][x + 1],
                                                             padded_array[y + 1][x + 1],
                                                             )
                sum = Orography.add_vectors(sum, triangle_normal)
                # fifth neighbour triangle
                triangle_normal = Orography.calculate_normal(padded_array[y][x],
                                                             padded_array[y + 1][x + 1],
                                                             padded_array[y + 1][x],
                                                             )
                sum = Orography.add_vectors(sum, triangle_normal)
                # sixth neighbour triangle
                triangle_normal = Orography.calculate_normal(padded_array[y][x],
                                                             padded_array[y + 1][x],
                                                             padded_array[y][x - 1],
                                                             )
                sum = Orography.add_vectors(sum, triangle_normal)
                sum = Orography.normalize(sum)
                row.append(sum)
            normals.append(row)
        return normals
