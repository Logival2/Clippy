import random


class Pig(object):
    def __init__(self):
        """ When relevant, 1 is the width of a chunk """
        self.reproduction_rate = random.uniform(0, .1)
        self.social_rate = random.uniform(0, 1)
        self.food_search_rate = random.uniform(0, 1)
        self.view_radius = random.uniform(.75, 100)

        self.hunger = 0 # dies if it reach 100
        self.urge_to_reproduce = 0
        self.sexe = random.randint(0, 1)
        """ Add a 'pheromone' map and add a curiosity factor """
