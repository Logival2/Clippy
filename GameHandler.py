import time
from collections import OrderedDict

from CliHandler import CliHandler
from MapHandler import MapHandler
from Entities import *
from utils import *


class GameHandler(object):
    def __init__(s, stdscr, seed=0):
        s.map_handler = MapHandler(seed)
        s.start_time = time.time()
        s.hud_infos = OrderedDict()
        s.hud_infos["CLIPPY"] = None
        s.hud_infos["separator"] = None
        s.hud_infos["score"] = 0
        s.hud_infos["empty"] = None
        s.hud_infos["time"] = int(time.time() - s.start_time)
        s.cli_handler = CliHandler(stdscr, fps=10)

    def launch(s):
        while 42:
            s.handle_inputs(s.cli_handler.get_inputs())
            s.handle_ia()
            s.hud_infos["time"] = int(time.time() - s.start_time)
            s.cli_handler.draw(s.map_handler, s.hud_infos)

    def handle_ia(s):
        return

    def handle_inputs(s, player_input):
        if not player_input or player_input not in ['z', 'q', 's', 'd']:
            return
        delta = None
        if player_input == 'z':   delta = Pos(-1, 0)
        elif player_input == 's': delta = Pos(1, 0)
        if player_input == 'q':   delta = Pos(0, -1)
        elif player_input == 'd': delta = Pos(0, 1)
        if delta and s.map_handler.move_entity_relative(s.map_handler.player_pos, delta):
            s.map_handler.player_pos += delta
