class Square(object):
    def __init__(s, low_ent, top_ent=None):
        s.low_ent = low_ent
        s.top_ent = top_ent
        s.is_free_flag = True if not s.top_ent or not s.top_ent.is_collider else False

    def is_free(s):
        s.is_free_flag = True if not s.top_ent or not s.top_ent.is_collider else False
        return s.is_free_flag

    def __repr__(s):
        if s.top_ent:
            return s.top_ent.__repr__()
        return s.low_ent.__repr__()


class Entity(object):
    def __init__(s, repr_char, is_collider=True, fg_color=39, bg_color=49):
        s.repr_char = repr_char
        s.fg_color = fg_color
        s.bg_color = bg_color
        s.is_collider = is_collider

    def __repr__(s):
        return f"\x1b[{s.bg_color};{s.fg_color}m{s.repr_char}\x1b[0m"

class Wall(Entity):
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

class Floor(Entity):
    pass
