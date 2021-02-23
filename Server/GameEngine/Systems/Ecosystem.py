import math
import random

from GameEngine.Components.Pig import Pig
from GameEngine.Components.Position import Position
from GameEngine.Components.Sprite import Sprite
from GameEngine.Components.Vegetable import Vegetable
from GameEngine.GameServer import ecs
from GameEngine.Components.Fox import Fox
from GameEngine.Components.Rabbit import Rabbit
from GameEngine.MapHandler.map_config import MAP_CONFIG

""" Multi process the AI """


def fox_update():
    """ What does the fow says ? """
    foxs = ecs.get_component(Fox)
    for fox in foxs:
        pass
    return {}


def food_finding(id):
    foods = ecs.filter(Vegetable, Position)
    veg = ecs.get_component(Vegetable)
    pos = ecs.get_component(Position)
    rabbit = ecs.get_component(Pig, id)

    nearby_food = []
    for food in foods:
        distance = math.dist([pos[id].x, pos[id].y],[pos[food].x, pos[food].y])
        if distance < rabbit.view_radius * MAP_CONFIG["chunk_size"]:
            nearby_food.append({"id": food, "dist": distance})

    nearby_food.sort(key=lambda a: a["dist"])


def rabbit_update():
    ids = ecs.filter(Pig, Position)
    pos = ecs.get_component(Position)

    for id in ids:
        food_finding(id)

    # if abs(social_direction[0] + food_direction[0]) > abs(social_direction[1] + food_direction[1]):
    #     if social_direction[0] + food_direction[0] > 0:
    #         positions[id].x += 1
    #     else:
    #         positions[id].x -= 1
    # else:
    #     if delta_y > 0:
    #         if social_direction[1] + food_direction[1] > 0:
    #             positions[id].y += 1
    #         else:
    #             positions[id].y -= 1
        select_direction = random.randint(0, 3)
        if select_direction == 0:
            pos[id].x += 1
        if select_direction == 1:
            pos[id].x -= 1
        if select_direction == 2:
            pos[id].y += 1
        if select_direction == 3:
            pos[id].y -= 1
    return {}
