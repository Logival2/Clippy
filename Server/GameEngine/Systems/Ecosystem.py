import math
import random

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


def rabbit_update():
    """ Rabbits will make different actions depending on their status """
    rabbit = ecs.get_component(Rabbit)
    vegetable = ecs.get_component(Vegetable)
    fox = ecs.get_component(Fox)
    positions = ecs.get_component(Position)
    rabbit_ids = ecs.filter(Rabbit, Position)
    fox_ids = ecs.filter(Fox, Position)
    food_ids = ecs.filter(Vegetable, Position)

    for id in rabbit_ids:
        food_direction = [0,0]
        fear_direction = [0,0]
        repr_direction = [0,0]

        """Living cost"""
        rabbit[id].hunger += 1
        rabbit[id].urge_to_reproduce += rabbit[id].reproduction_rate
        if rabbit[id].hunger >= 100:
            # ecs.delete_id(id)
            continue

        """Can it eat ?"""
        for food in food_ids:
            if positions[id] == positions[food]:
                rabbit[id].hunger = min(0, rabbit[id].hunger - vegetable[food].nutritionnal_score)

        """Social intelligence"""
        rep_mate = {}
        rep_direction = [0, 0, 0]
        social_direction = [0, 0, 0]
        for mate in rabbit_ids:
            dist = math.dist([positions[id].x,positions[id].y], [positions[mate].x,positions[mate].y])
            if dist < rabbit[id].view_radius * MAP_CONFIG["chunk_size"] and mate is not id:
                if rabbit[mate].sexe is not rabbit[id].sexe:
                    rep_mate[mate] = dist
                    rep_direction[0] += positions[mate].x
                    rep_direction[1] += positions[mate].y
                    rep_direction[2] += 1
                social_direction[0] += positions[mate].x
                social_direction[1] += positions[mate].y
                social_direction[2] += 1
        rep_direction[0] /= (rep_direction[2] if rep_direction[2] != 0 else 1)
        rep_direction[1] /= (rep_direction[2] if rep_direction[2] != 0 else 1)
        social_direction[0] /= (social_direction[2] if rep_direction[2] != 0 else 1)
        social_direction[1] /= (social_direction[2] if rep_direction[2] != 0 else 1)
        delta_x = (social_direction[0]*rabbit[id].social_rate + rep_direction[0]*rabbit[id].urge_to_reproduce) - positions[id].x
        delta_y = (social_direction[1]*rabbit[id].social_rate + rep_direction[1]*rabbit[id].urge_to_reproduce) - positions[id].y

        """Predator fear"""

        for fear in food_ids:
            fear_direction


        if abs(delta_x) > abs(delta_y):
            if delta_x > 0:
                positions[id].x += 1
            else:
                positions[id].x -= 1
        else:
            if delta_y > 0:
                positions[id].y += 1
            else:
                positions[id].y -= 1
        # select_direction = random.randint(0, 3)
        # if select_direction == 0:
        #     positions[id].x += 1
        # if select_direction == 1:
        #     positions[id].x -= 1
        # if select_direction == 2:
        #     positions[id].y += 1
        # if select_direction == 3:
        #     positions[id].y -= 1
    return positions
