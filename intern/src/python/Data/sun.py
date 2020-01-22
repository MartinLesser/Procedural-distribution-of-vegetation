import math


class Sun:
    def __init__(self, elevation, azimuth):
        self.elevation = elevation
        self.azimuth = azimuth

    def convert_to_uv_coordinates(self):
        """
        Transforms the polar coordinates of the sun to cartesian coordinates.
        :return: cartesian coordinates.
        """
        u = math.cos(math.radians(self.azimuth)) * math.cos(math.radians(self.elevation))
        v = math.sin(math.radians(self.azimuth)) * math.cos(math.radians(self.elevation))
        w = math.sin(math.radians(self.elevation))
        u = round(u, 4)
        v = round(v, 4)
        w = round(w, 4)
        return u, v, w
