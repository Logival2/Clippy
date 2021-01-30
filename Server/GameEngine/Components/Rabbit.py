import random

from GameEngine.Components.Position import Position
from GameEngine.GameServer import ecs


class Rabbit:
    def __init__(self):
        """ When relevant, 1 is the width of a chunk """
        self.reproduction_rate = random.uniform(0, 1)
        self.social_rate = random.uniform(0, 1)
        self.food_search_rate = random.uniform(0, 1)
        self.view_radius = random.uniform(0, 0.25)

        self.hunger = 0
        self.urge_to_reproduce = 0
        """ Add a 'pheromone' map and add a curiosity factor """


def rabbit_update():
    """ Rabbits will make different actions depending on their status """
    rabbits = ecs.get_component(Rabbit)
    positions = ecs.get_component(Position)
    ids = ecs.filter(Rabbit, Position)
    for id in ids:
        select_direction = random.randint(0, 3)
        if select_direction == 0:
            positions[id].x += 1
        if select_direction == 1:
            positions[id].x -= 1
        if select_direction == 2:
            positions[id].y += 1
        if select_direction == 3:
            positions[id].y -= 1
    return positions
