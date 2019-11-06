import numpy as np

from coordinates import Coordinates


class Animal:
    def __init__(self, coordinates, environment, vision_radius=1, weights=None):
        self.coordinates = coordinates
        self.environment = environment
        self.vision_radius = vision_radius
        self.hunger = 7
        self.weights = np.random.randn(vision_radius*2 + 1, vision_radius*2 + 1, 5).reshape(-1, 5)
        self.time = 0
        self.eat_times = 0
        if weights is not None:
            self.weights = weights

    def move(self, new_coordinates):
        if self.environment.is_coordinate_availible(new_coordinates):
            self.coordinates = new_coordinates

    def move_right(self):
        new_coordinates = Coordinates(self.coordinates.height_coord, self.coordinates.width_coord+1)
        self.move(new_coordinates)

    def move_left(self):
        new_coordinates = Coordinates(self.coordinates.height_coord, self.coordinates.width_coord-1)
        self.move(new_coordinates)

    def move_up(self):
        new_coordinates = Coordinates(self.coordinates.height_coord-1, self.coordinates.width_coord)
        self.move(new_coordinates)

    def move_down(self):
        new_coordinates = Coordinates(self.coordinates.height_coord+1, self.coordinates.width_coord)
        self.move(new_coordinates)

    def eat(self):
        if self.environment.eat(self.coordinates):
            self.hunger += 7
            self.eat_times += 1

    def act(self):
        vision = self.environment.get_vision(self.coordinates, self.vision_radius)
        trees = (vision == 1).flatten().reshape(1, -1)
        scores = trees.dot(self.weights)
        action = np.argmax(scores)
        if action == 0:
            self.move_up()
        elif action == 1:
            self.move_down()
        elif action == 2:
            self.move_left()
        elif action == 3:
            self.move_right()
        elif action == 4:
            self.eat()
        self.hunger -= 1
        self.time += 1
