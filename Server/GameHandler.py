import time
from collections import OrderedDict

from Displayers.CliDisplay import CliDisplay
from Displayers.PyGame.PyGameDisplay import PyGameDisplay
from GameEngine.Ecs import Ecs
from MapHandler import MapHandler
from Entities import *
from utils import *


class GameHandler(object):
    def __init__(s, stdscr, seed=0):
        s.map_handler = MapHandler(seed)
        s.start_time = time.time()
        s.hud_infos = OrderedDict()
        s.hud_infos["score"] = 0
        s.hud_infos["time"] = int(time.time() - s.start_time)
        # s.cli_handler = CliDisplay(stdscr, fps=10)
        s.cli_handler = PyGameDisplay(fps=4, target_resolution=Pos(x=1800, y=1000))
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
        player_inputs = s.cli_handler.get_inputs()
        if not player_inputs: return
        if "EXIT" in player_inputs: exit()
        for player_input in player_inputs:
            if player_input in s.avail_inputs.keys():
                if s.map_handler.move_entity_relative(s.map_handler.player_pos, s.avail_inputs[player_input]):
                    s.map_handler.player_pos += s.avail_inputs[player_input]
                    break
