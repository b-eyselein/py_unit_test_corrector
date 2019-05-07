from math import pi


class Circle:
    def __init__(self, center_x: float, center_y: float, radius: float):
        if not isinstance(center_x, float) and not isinstance(center_x, int):
            raise Exception("Die x-Koordinate muss eine Zahl sein!")

        self.center_x: float = center_x

        if not isinstance(center_y, float) and not isinstance(center_y, int):
            raise Exception("Die y-Koordinate muss eine Zahl sein!")

        self.center_y: float = center_y

        if not isinstance(radius, float) and not isinstance(radius, int):
            raise Exception("Der Radius muss eine Zahl sein!")

        if radius < 0:
            raise Exception("Der Radius muss größer als 0 sein!")

        self.radius: float = radius

    def area(self) -> float:
        return pi * self.radius * self.radius
