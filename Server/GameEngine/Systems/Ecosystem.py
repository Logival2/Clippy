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
    pig = ecs.get_component(Pig)
    veg = ecs.get_component(Vegetable)
    pos = ecs.get_component(Position)
    rabbit = ecs.get_component(Pig, id)

    nearby_food = []
    for food in foods:
        distance = math.dist([pos[id].x, pos[id].y],[pos[food].x, pos[food].y])
        if distance < rabbit.view_radius * MAP_CONFIG["chunk_size"]:
            nearby_food.append({"id": food, "dist": distance})

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
        distance = math.dist([pos[id].x, pos[id].y], [pos[mate].x, pos[mate].y])
        if distance < rabbit.view_radius * MAP_CONFIG["chunk_size"]:
            interests.append({"id": mate, "dist": distance})

    return interests


def rabbit_update():
    ids = ecs.filter(Pig, Position)
    pos = ecs.get_component(Position)
    choice = []
    for id in ids:
        choice += food_finding(id)
        choice += social_interests(id)

        if len(choice) > 0:
            rd = choice[0]
            # if abs(pos[rd["id"]].x - pos[id].x) > abs(pos[rd["id"]].y - pos[id].y):
            if pos[rd["id"]].x - pos[id].x > 0:
                pos[id].x += 1
            else:
                pos[id].x -= 1
            # if pos[rd["id"]].x - pos[id].x > 0:
            if pos[rd["id"]].y - pos[id].y > 0:
                pos[id].y += 1
            else:
                pos[id].y -= 1
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
