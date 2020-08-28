class Entity(object):
    def __init__(s, repr_char, fg_color=39, bg_color=49):
        s.repr_char = repr_char
        s.fg_color = fg_color
        s.bg_color = bg_color

    def __repr__(s):
        return f"\x1b[{s.bg_color};{s.fg_color}m{s.repr_char}"

class Obstacle(Entity):
    pass

# Alive entities
class LivingEntity(Entity):
    def __init__(s, repr_char, fg_color=39, bg_color=49, name="default_name"):
        super(LivingEntity, s).__init__(repr_char, fg_color, bg_color)
        s.name = name

class Player(LivingEntity):
    pass

class Enemy(LivingEntity):
    pass
