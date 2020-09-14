class Square(object):
    def __init__(s, noise_value, low_ent, top_ent):
        s.low_ent = low_ent
        s.top_ent = top_ent
        s.noise_value = noise_value

        s.is_free_flag = s.is_free()

    def is_free(s):
        s.is_free_flag = False
        if not s.top_ent or not s.top_ent.is_collider:
            if not s.low_ent or not s.low_ent.is_collider:
                s.is_free_flag = True
        return s.is_free_flag

    def get_colors(s):
        if s.top_ent:
            if s.top_ent.bg_color == -1:  # If top ent has a transparent background
                return (s.top_ent.fg_color, s.low_ent.bg_color)
            return (s.top_ent.fg_color, s.top_ent.bg_color)
        return (s.low_ent.fg_color, s.low_ent.bg_color)

    def get_char(s):
        if s.top_ent:
            return s.top_ent.repr_char
        return s.low_ent.repr_char

    def get_types(s):
        if s.top_ent and s.low_ent:
            return (s.top_ent.type, s.low_ent.type)
        if s.top_ent:
            return (s.top_ent.type, None)
        return (None, s.low_ent.type)

class Entity(object):
    def __init__(s, type, is_collider):
        s.type = type
        s.is_collider = is_collider

# Alive entities
class LivingEntity(Entity):
    def __init__(s, type, is_collider, name="default_name"):
        super(LivingEntity, s).__init__(type, is_collider)
        s.name = name


class Player(LivingEntity):
    pass


class Enemy(LivingEntity):
    pass
