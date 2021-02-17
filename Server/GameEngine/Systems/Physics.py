from GameEngine.Components.Hitbox import Hitbox
from GameEngine.Components.Position import Position
from GameEngine.GameServer import ecs

def does_collide(pos, ids, positions):
    for collide in ids:
        if pos == positions[collide] and id != collide:
            return True
    return False


def hitbox_update():
    ids = ecs.filter(Hitbox, Position)
    positions = ecs.get_component(Position)
    hitboxs = ecs.get_component(Hitbox)

    for id in ids:
        for collide in ids:
            if positions[id] == positions[collide] and id != collide:
                if not does_collide(Position(x=hitboxs[id].x, y=positions[id].y), ids, positions):
                    positions[id].x = hitboxs[id].x
                elif not does_collide(Position(x=positions[id].x, y=hitboxs[id].y), ids, positions):
                    positions[id].y = hitboxs[id].y

    for id in ids:
        hitboxs[id].x = positions[id].x
        hitboxs[id].y = positions[id].y
    return {}