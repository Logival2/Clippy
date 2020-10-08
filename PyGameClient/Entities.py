class Tile(object):
    def __init__(s, noise_value, low_ent, top_ent):
        s.low_ent = low_ent
        s.top_ent = top_ent
        # Provided to the displayers for consistent variations of sprites
        s.noise_value = noise_value
        # Regions are stored in the Entities
        # as moving entities can move and need to have their region 'with them'
        # Layout is however linked to the Tiles themselves, as it only affects the terrain

    def is_free(s):
        if not s.top_ent: return True

    def get_types(s):
        if s.top_ent and s.low_ent:
            return (s.top_ent.type, s.low_ent.type)
        if s.top_ent:
            return (s.top_ent.type, None)
        return (None, s.low_ent.type)

class Entity(object):
    def __init__(s, type, region=0):
        s.type = type
        s.region = region

# Alive entities
class LivingEntity(Entity):
    def __init__(s, type, region, name="default_name"):
        super(LivingEntity, s).__init__(type, region)
        s.name = name

class Player(LivingEntity):
    pass


class Enemy(LivingEntity):
    pass

### BLOCKS ###
class Grass(Entity):
    def __init__(self, noise_value, region):
        super(Grass, self).__init__('grass', region)

class Gravel(Entity):
    def __init__(self, noise_value, region):
        super(Gravel, self).__init__('gravel', region)

class Lava(Entity):
    def __init__(self, noise_value, region):
        super(Lava, self).__init__('lava', region)

class Sand(Entity):
    def __init__(self, noise_value, region):
        super(Sand, self).__init__('sand', region)

class Stone(Entity):
    def __init__(self, noise_value, region):
        super(Stone, self).__init__('stone', region)

class Water(Entity):
    def __init__(self, noise_value, region):
        super(Water, self).__init__('water', region)
