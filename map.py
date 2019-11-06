import numpy as np

from coordinates import Coordinates


class Map:
    def __init__(self, height, width, shift=20):
        self.field = np.zeros([height+shift*2, width+shift*2])
        self.field[:shift] = 2
        self.field[-shift:] = 2
        self.field[:, :shift] = 2
        self.field[:, -shift:] = 2

        self.number_of_trees = 0

    def _set_value(self, coordinates, value):
        self.field[coordinates.height_coord, coordinates.width_coord] = value

    def generate_tree(self, coordinates):
        if not self.is_cell_empty(coordinates):
            return
        self._set_value(coordinates, 1)
        self.number_of_trees += 1

    def eat_tree(self, coordinates):
        if self.field[coordinates.height_coord, coordinates.width_coord] == 1:
            self._set_value(coordinates, 0)
            self.number_of_trees -= 1
            return 1
        return 0

    def is_cell_empty(self, coordinates):
        return self.field[coordinates.height_coord, coordinates.width_coord] == 0

    def is_cell_availible(self, coordinates):
        return self.field[coordinates.height_coord, coordinates.width_coord] < 2

    def get_random_coordinates(self):
        height_coord = np.random.randint(0, self.field.shape[0] - 1)
        width_coord = np.random.randint(0, self.field.shape[1] - 1)
        coordinates = Coordinates(height_coord, width_coord)
        if not self.is_cell_empty(coordinates):
            return self.get_random_coordinates()
        return coordinates

    def generete_random_tree(self):
        coordinates = self.get_random_coordinates()
        self.generate_tree(coordinates)

    def get_vision(self, coordinates, radius):
        h_low_coordinate = coordinates.height_coord - radius
        h_high_coordinate = coordinates.height_coord + radius + 1

        w_low_coordinate = coordinates.width_coord - radius
        w_high_coordinate = coordinates.width_coord + radius + 1
        vision_map = self.field[h_low_coordinate: h_high_coordinate, w_low_coordinate:w_high_coordinate]
        return vision_map


