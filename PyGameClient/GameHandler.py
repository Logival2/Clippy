import time
from collections import OrderedDict
import queue

from NetworkManager import NetworkManager
from Displayer.PyGameDisplay import PyGameDisplay
from MapHandler import MapHandler
from Entities import *
from utils import *
from config import MAP_CONFIG, DISPLAY_CONFIG


class GameHandler(object):
    def __init__(s):
        random.seed(MAP_CONFIG['seed'])
        ### MAP ###
        s.map_handler = MapHandler(MAP_CONFIG)
        ### DISPLAY ###
        s.display_m = PyGameDisplay(DISPLAY_CONFIG)
        ### HUD ###
        s.start_time = time.time()
        s.hud_infos = OrderedDict()
        s.hud_infos["score"] = 0
        s.hud_infos["time"] = int(time.time() - s.start_time)
        ### MOVEMENTS ###
        s.avail_inputs = {
            'UP': Pos(-1, 0),
            'DOWN': Pos(1, 0),
            'LEFT': Pos(0, -1),
            'RIGHT': Pos(0, 1),
        }
        ### NETWORK ###
        s.receive_q = queue.Queue(maxsize=0)
        s.send_q = queue.Queue(maxsize=0)
        try:
            s.network_m = NetworkManager(
                                s.receive_q, s.send_q,
                                '127.0.0.1', 65432,
                            )
            s.network_thread = s.network_m.run()
        except Exception as e:
            print(f'Failed networkmanager init: {e}')
        else:
            print(f'Connected to 127.0.0.1:65432')
        # s.send_q.put([1, 'jesuisuntest'])


    def launch(s):
        while 42:
            s.handle_network()
            s.handle_inputs()
            s.handle_ia()
            s.hud_infos["time"] = int(time.time() - s.start_time)
            s.display_m.draw(s.map_handler, s.hud_infos)

    def handle_ia(s):
        return

    def handle_network(s):
        s.send_q.put([200, s.hud_infos["time"]])
        while not s.receive_q.empty():
            print("received:", s.receive_q.get())

    def handle_inputs(s):
        """ Exit if needed, otherwise try to execute the first move, if not successful (collision)
        try the next one etc, otherwise return """
        player_inputs = s.display_m.get_inputs()
        if not player_inputs: return
        if "EXIT" in player_inputs: exit()
        for player_input in player_inputs:
            if player_input in s.avail_inputs.keys():
                if s.map_handler.move_entity_relative(s.map_handler.player_pos, s.avail_inputs[player_input]):
                    s.map_handler.player_pos += s.avail_inputs[player_input]
                    break
