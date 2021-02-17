from GameEngine.Components.Stat import Stat
from GameEngine.GameServer import ecs


def stat_update():
    elems = ecs.getComponent(Stat)

    for k, v in elems:
        if v.health < 0:
            ecs.delete_id(k)
