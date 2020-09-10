class Square(object):
    def __init__(s, low_ent, top_ent=None):
        s.low_ent = low_ent
        s.top_ent = top_ent
        s.is_free_flag = s.is_free()

    def is_free(s):
        s.is_free_flag = True if not s.top_ent or not s.top_ent.is_collider else False
        return s.is_free_flag

    def get_colors(s):
        if s.top_ent:
            if s.top_ent.bg_color == -1:  # If top ent has a transparent background
                # exit()
                return (s.top_ent.fg_color, s.low_ent.bg_color)
            return (s.top_ent.fg_color, s.top_ent.bg_color)
        return (s.low_ent.fg_color, s.low_ent.bg_color)

    def get_char(s):
        if s.top_ent:
            return s.top_ent.repr_char
        return s.low_ent.repr_char


class Entity(object):
    def __init__(s, repr_char, fg_color, bg_color, is_collider=True):
        s.repr_char = repr_char
        s.fg_color = fg_color
        s.bg_color = bg_color
        s.is_collider = is_collider


class Wall(Entity):
    pass


# Alive entities
class LivingEntity(Entity):
    def __init__(s, repr_char, fg_color, bg_color, is_collider=True, name="default_name"):
        super(LivingEntity, s).__init__(repr_char, fg_color, bg_color, is_collider)
        s.name = name


class Player(LivingEntity):
    pass


class Enemy(LivingEntity):
    pass
