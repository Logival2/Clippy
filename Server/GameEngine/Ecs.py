from GameEngine.MapHandler import MapHandler


class Ecs(object):
    def __init__(s):
        s.components = {}
        s.updates = []
        s.entity = 0
        s.map_handler = MapHandler()

    def new_entity(s):
        s.entity += 1
        return s.entity

    def get_component(s, component, entity=None):
        if type(component()).__name__ not in s.components:
            print("No component " + type(component()).__name__ + " stored.")
            return []
        if entity is None:
            return s.components[type(component()).__name__]
        return next(item for item in s.components[type(component()).__name__] if item["entity"] == entity)

    def add_component(s, entity, component):
        if type(component).__name__ not in s.components:
            s.components[type(component).__name__] = []
        s.components[type(component).__name__].append({"entity": entity, "component": component})

    def add_update(s, function):
        s.updates.append(function)

    def update(s):
        for function in s.updates:
            function()


ecs = Ecs()

if __name__ == '__main__':
    ecs = Ecs()

    ecs.add_component(7, int())
    print(ecs.get_component(int))
    ecs.add_update(lambda: print("mesboules"))
    ecs.update()
