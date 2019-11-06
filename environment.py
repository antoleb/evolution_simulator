import random
import numpy as np

from animal import Animal

import subprocess as sp
import time


class Environment:
    def __init__(self, map):
        self.map = map
        self.animal_dict = {}
        self.best_animals = {}
        self.time = 0
        self.number_of_animals = 900
        self.is_interesting = False
        self.max_eat_time = 0
        self.current_eat_time = 0
        self.number_of_trees = 4000
        self.number_of_best_animals = 4000
        self._living_time = 0
        self.interesting_times = 1000

    def add_animal(self):
        identifier = random.randint(0, 1e9)
        while identifier in self.animal_dict:
            identifier = random.randint(0, 1e9)
        coordinates = self.map.get_random_coordinates()
        animal = Animal(coordinates, self)
        self.animal_dict[identifier] = animal

    def eat(self, coordinates):
        return self.map.eat_tree(coordinates)

    def is_coordinate_availible(self, coordinates):
        return self.map.is_cell_availible(coordinates)

    def kill_animal(self, animal_id):
        animal = self.animal_dict[animal_id]
        self.best_animals[animal.eat_times] = animal
        while len(self.best_animals) > self.number_of_best_animals:
            worst_time = min(list(self.best_animals.keys()))
            del self.best_animals[worst_time]

        del self.animal_dict[animal_id]

    def act(self):
        animal_to_kill = []
        self.is_interesting = False
        for animal_id, animal in self.animal_dict.items():
            animal.act()
            if animal.eat_times > self.interesting_times:
                self.is_interesting = True
            self.max_eat_time = max(self.max_eat_time, animal.eat_times)
            self.current_eat_time = max(self.current_eat_time, animal.eat_times)
            if animal.hunger <= 0:
                animal_to_kill.append(animal_id)
        for animal_id in animal_to_kill:
            self.kill_animal(animal_id)

        if len(animal_to_kill) == 0:
            self._living_time += 1
        else:
            self._living_time = 0
        if self._living_time > 10:
            self.number_of_trees -= 1

        while self.map.number_of_trees < self.number_of_trees:
            self.map.generete_random_tree()
        self.time += 1
        self.generate_animals()

    def get_vision(self, coordinates, vision_radius):
        return self.map.get_vision(coordinates, vision_radius)

    def generate_animals(self):
        while len(self.animal_dict) < self.number_of_animals:
            if len(self.animal_dict) == 0:
                self.add_animal()
                continue
            animals = list(self.animal_dict.values())
            animals.extend(self.best_animals.values())
            living_times = np.array([animal.eat_times for animal in animals])
            living_times = (living_times+1e-3) / (living_times.sum() + 1e-3)
            living_times /= living_times.sum()

            mother = np.random.choice(animals, p=living_times)
            father = np.random.choice(animals, p=living_times)
            k = np.random.rand(*mother.weights.shape)
            mutation = np.random.randn(*mother.weights.shape)
            new_weights = k * mother.weights + (1-k)*father.weights
            new_weights += mutation

            identifier = random.randint(0, 1e9)
            while identifier in self.animal_dict:
                identifier = random.randint(0, 1e9)
            coordinates = self.map.get_random_coordinates()
            animal = Animal(coordinates, self, weights=new_weights)
            self.animal_dict[identifier] = animal

    def print_map(self):
        _ = sp.call('clear', shell=True)
        field = self.map.field.copy()
        for animal in self.animal_dict.values():
            field[animal.coordinates.height_coord, animal.coordinates.width_coord] = -1
            if animal.eat_times > self.interesting_times:
                field[animal.coordinates.height_coord, animal.coordinates.width_coord] = -2
        for line in field:
            for char in line:
                if char == -2:
                    print('A', end='')
                if char == -1:
                    print('a', end='')
                if char == 0:
                    print(' ', end='')
                if char == 1:
                    print('t', end='')
                if char == 2:
                    print('x', end='')
            print()

    def run(self):
        while True:
            self.act()
            # print(self.time)
            if self.time % 10 == 0:
                print(self.time, self.max_eat_time, self.current_eat_time, self.number_of_trees,
                      len(self.best_animals), self.number_of_animals, len(self.animal_dict))
                self.current_eat_time = 0
                self.number_of_animals -= 1
            if self.is_interesting:
                self.print_map()
                time.sleep(0.3)


