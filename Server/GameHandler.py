import time
from collections import OrderedDict

from Displayers.CliDisplay import CliDisplay
from Displayers.PyGame.PyGameDisplay import PyGameDisplay
from GameEngine.Ecs import Ecs
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
        s.cli_handler = PyGameDisplay(DISPLAY_CONFIG)
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
        s.ecs = Ecs()
        s.ecs.add_update(s.handle_inputs)
        s.ecs.add_update(s.handle_ia)
        s.ecs.add_update(s.handle_hud)
        s.ecs.add_update(s.handle_display)

    def launch(s):
        while 42:
            s.ecs.update()

    def handle_hud(s):
        s.hud_infos["time"] = int(time.time() - s.start_time)

    def handle_display(s):
        s.cli_handler.draw(s.map_handler, s.hud_infos)

    def handle_ia(s):
        return

    def handle_inputs(s):
        """ Exit if needed, otherwise try to execute the first move, if not successful (collision)
        try the next one etc, otherwise return """
        player_inputs = s.cli_handler.get_inputs()
        if not player_inputs: return
        if "EXIT" in player_inputs: exit()
        for player_input in player_inputs:
            if player_input in s.avail_inputs.keys():
                if s.map_handler.move_entity_relative(s.map_handler.player_pos, s.avail_inputs[player_input]):
                    s.map_handler.player_pos += s.avail_inputs[player_input]
                    break
