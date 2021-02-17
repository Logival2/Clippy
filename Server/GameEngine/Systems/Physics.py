from GameEngine.Components.Hitbox import Hitbox
from GameEngine.Components.Position import Position
from GameEngine.GameServer import ecs


def hitbox_update():
    ids = ecs.filter(Hitbox, Position)
    positions = ecs.get_component(Position)
    hitboxs = ecs.get_component(Hitbox)

    for id in ids:
        for collide in ids:
            if positions[id] == positions[collide] and id != collide:
                positions[id].x = hitboxs[id].x
                positions[id].y = hitboxs[id].y

    for id in ids:
        hitboxs[id].x = positions[id].x
        hitboxs[id].y = positions[id].y
    return {}