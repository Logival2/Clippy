import random

from Server.GameEngine.Ecs import ecs


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
    for rabbit in rabbits:
        select_dialog = random.randint(0, 2)
        if select_dialog == 0:
            print("SKYA")
        if select_dialog == 1:
            print("Skuuu")
        if select_dialog == 2:
            print("YEET")
