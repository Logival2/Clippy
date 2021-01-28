from GameEngine.Ecs import ecs


def receive():
    print("Bonjour, je reçois de la donné")
    return ["donné 1", "donné 2"]


def send(data):
    print("Bonjour, je yeet la donné: ", data)


def network_update():
    print("in")
    received = receive()
    for elem in received:
        print("je fais un truc", elem)

    send(["Position 1", "Position 2", "Position 3"])
