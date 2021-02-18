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


def rabbit_update():
    """ FULL REWORK """
    rabbit = ecs.get_component(Pig)
    vegetable = ecs.get_component(Vegetable)
    fox = ecs.get_component(Fox)
    positions = ecs.get_component(Position)
    rabbit_ids = ecs.filter(Pig, Position)
    fox_ids = ecs.filter(Fox, Position)
    food_ids = ecs.filter(Vegetable, Position)

    for id in rabbit_ids:
        food_direction = [0,0,0]
        fear_direction = [0,0,0]
        social_direction = [0,0,0]

        """Living cost"""
        rabbit[id].hunger += 1
        rabbit[id].urge_to_reproduce += rabbit[id].reproduction_rate
        if rabbit[id].hunger >= 100:
            # ecs.delete_id(id)
            # continue
            pass

        """Can it eat ?"""
        for food in food_ids:
            if positions[id] == positions[food]:
                rabbit[id].hunger = min(0, rabbit[id].hunger - vegetable[food].nutritionnal_score)

        """Social intelligence"""
        rep_mate = {}
        rep_direction = [0, 0, 0]
        for mate in rabbit_ids:
            dist = math.dist([positions[id].x,positions[id].y], [positions[mate].x,positions[mate].y])
            if dist < rabbit[id].view_radius * MAP_CONFIG["chunk_size"] and mate is not id:
                if rabbit[mate].sexe is not rabbit[id].sexe:
                    rep_mate[mate] = dist
                    rep_direction[0] += positions[mate].x - positions[id].x
                    rep_direction[1] += positions[mate].y - positions[id].y
                    rep_direction[2] += 1
                social_direction[0] += positions[mate].x - positions[id].x
                social_direction[1] += positions[mate].y - positions[id].y
                social_direction[2] += 1
        rep_direction[0] /= (rep_direction[2] if rep_direction[2] != 0 else 1)
        rep_direction[1] /= (rep_direction[2] if rep_direction[2] != 0 else 1)
        social_direction[0] /= (social_direction[2] if rep_direction[2] != 0 else 1)
        social_direction[1] /= (social_direction[2] if rep_direction[2] != 0 else 1)
        social_direction[0] = (social_direction[0]*rabbit[id].social_rate + rep_direction[0]*rabbit[id].urge_to_reproduce)
        social_direction[1] = (social_direction[1]*rabbit[id].social_rate + rep_direction[1]*rabbit[id].urge_to_reproduce)

        """Food Searching"""
        closest = 0
        closest_score = 1000000000

        for food in food_ids:
            dist = math.dist([positions[id].x, positions[id].y], [positions[food].x, positions[food].y])
            if dist < rabbit[id].view_radius * MAP_CONFIG["chunk_size"] and food is not id:
                if dist < closest_score:
                    closest_score = dist
                    closest = food
                food_direction[0] += positions[food].x - positions[id].x
                food_direction[1] += positions[food].y - positions[id].y
        food_direction[0] = (food_direction[0] / (food_direction[2] if food_direction[2] != 0 else 1)) * 0.2 + (positions[closest].x - positions[id].x) * 0.8
        food_direction[1] = (food_direction[1] / (food_direction[2] if food_direction[2] != 0 else 1)) * 0.2 + (positions[closest].y - positions[id].y) * 0.8

        """Predator fear"""

        for fear in food_ids:
            fear_direction


        if abs(social_direction[0] + food_direction[0]) > abs(social_direction[1] + food_direction[1]):
            if social_direction[0] + food_direction[0] > 0:
                positions[id].x += 1
            else:
                positions[id].x -= 1
        else:
            if social_direction[1] + food_direction[1] > 0:
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
