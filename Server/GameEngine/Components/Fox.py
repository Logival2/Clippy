import random

from GameEngine.GameServer import ecs


class Fox:
    def __init__(self):
        """ When relevant, 1 is the width of a chunk """
        """ Properties will change during AI tweaks """
        self.reproduction_rate = random.uniform(0, 1)
        self.social_rate = random.uniform(0, 1)
        self.food_search_rate = random.uniform(0, 1)
        self.view_radius = random.uniform(0, 0.5)

        self.hunger = 0
        self.urge_to_reproduce = 0
        """ Add a 'pheromone' map and add a curiosity factor """
