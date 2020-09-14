import time
from collections import OrderedDict

from Displayers.CliDisplay import CliDisplay
from Displayers.PyGame.PyGameDisplay import PyGameDisplay
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

    def launch(s):
        while 42:
            s.handle_inputs()
            s.handle_ia()
            s.hud_infos["time"] = int(time.time() - s.start_time)
            s.cli_handler.draw(s.map_handler, s.hud_infos)

    def handle_ia(s):
        return

    def handle_inputs(s):
        player_input = s.cli_handler.get_inputs()
        if player_input == "EXIT": exit()
        if not player_input: return
        delta = None
        if player_input == 'UP':   delta = Pos(-1, 0)
        elif player_input == 'DOWN': delta = Pos(1, 0)
        if player_input == 'LEFT':   delta = Pos(0, -1)
        elif player_input == 'RIGHT': delta = Pos(0, 1)
        if delta and s.map_handler.move_entity_relative(s.map_handler.player_pos, delta):
            s.map_handler.player_pos += delta
