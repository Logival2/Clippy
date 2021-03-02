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


def retrieve_nearby(id, types, dist):
    ret = {}
    pos = ecs.get_component(Position)

    if type(types) != list:
        types = [types]

    for tipe in types:
        elems = ecs.filter(tipe)
        nearby = []
        for elem in elems:
            distance = math.dist([pos[id].x, pos[id].y], [pos[elem].x, pos[elem].y])
            if distance < dist:
                nearby.append({"id": elem, "dist": distance})
        ret[tipe.__name__] = nearby

    return ret


def fox_update():
    """ What does the fow says ? """
    foxs = ecs.get_component(Fox)
    for fox in foxs:
        pass
    return {}


def food_finding(id):
    pig = ecs.get_component(Pig)
    veg = ecs.get_component(Vegetable)
    rabbit = ecs.get_component(Pig, id)

    nearby_food = retrieve_nearby(id, Vegetable, rabbit.view_radius * MAP_CONFIG["chunk_size"])["Vegetable"]

    nearby_food.sort(key=lambda a: a["dist"])

    if len(nearby_food) and nearby_food[0]["dist"] <= 1.6:
        pig[id].hunger -= veg[nearby_food[0]["id"]].nutritionnal_score
        ecs.id_delete.append(nearby_food[0]["id"])

    return nearby_food

def social_interests(id):
    interests = []
    mates = ecs.filter(Vegetable, Position)
    pig = ecs.get_component(Pig)
    veg = ecs.get_component(Vegetable)
    pos = ecs.get_component(Position)
    rabbit = ecs.get_component(Pig, id)

    for mate in mates:
        if id != mate:
            continue
        distance = math.dist([pos[id].x, pos[id].y], [pos[mate].x, pos[mate].y])
        if distance < rabbit.view_radius * MAP_CONFIG["chunk_size"]:
            interests.append({"id": mate, "dist": distance})

    return interests


def rabbit_update():
    ids = ecs.filter(Pig, Position)
    pos = ecs.get_component(Position)
    pigs = ecs.get_component(Pig)
    vegs = ecs.get_component(Vegetable)

    for id in ids:
        pig = pigs[id]
        nearby = retrieve_nearby(id, [Pig, Fox, Vegetable], pig.view_radius * MAP_CONFIG["chunk_size"])
        escape = False

        pig.hunger += 1
        if pig.hunger >= 100:
            ecs.id_delete.append(id)
            continue
        """ Eat nearby food if possible"""
        nearby["Vegetable"].sort(key=lambda a: a["dist"])

        if len(nearby["Vegetable"]) and nearby["Vegetable"][0]["dist"] <= 1.6:
            pig.hunger -= vegs[nearby["Vegetable"][0]["id"]].nutritionnal_score
            ecs.id_delete.append(nearby["Vegetable"][0]["id"])

        """ Choose action depending on current stats """
        if len(nearby["Pig"]) != 0:
            escape = True
            choice = nearby["Fox"]
        elif len(nearby["Vegetable"]) != 0 and pig.hunger * 2 < nearby["Vegetable"][0]["dist"]:
            choice = nearby["Vegetable"]
        elif len(nearby["Pig"]) != 0 and pig.urge_to_reproduce > pig.reproduction_rate:
            choice = nearby["Pig"]
        else:
            _, choice = random.choice(list(nearby.items()))

        if len(choice) > 0:
            rd = choice[0]
            # if abs(pos[rd["id"]].x - pos[id].x) > abs(pos[rd["id"]].y - pos[id].y):
            if pos[rd["id"]].x - pos[id].x > 0:
                pos[id].x += 1 if not escape else -1
            else:
                pos[id].x -= 1 if not escape else -1
            # if pos[rd["id"]].x - pos[id].x > 0:
            if pos[rd["id"]].y - pos[id].y > 0:
                pos[id].y += 1 if not escape else -1
            else:
                pos[id].y -= 1 if not escape else -1
        else:
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
