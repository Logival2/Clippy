import time
from collections import OrderedDict

from CliHandler import CliHandler
from MapHandler import MapHandler
from Entities import *
from utils import Pos


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
        s.cli_handler = CliHandler(stdscr, fps=20)

    def launch(s):
        while 42:
            s.handle_inputs(s.cli_handler.get_inputs())
            s.handle_ia()
            s.hud_infos["time"] = int(time.time() - s.start_time)
            s.cli_handler.draw(s.map_handler, s.hud_infos)

    def handle_ia(s):
        return

    def handle_inputs(s, inputs):
        for last_input in inputs[-2:]:
            if not last_input in ['z', 'q', 's', 'd']: continue
            delta = None
            if last_input == 'z':   delta = Pos(-1, 0)
            elif last_input == 's': delta = Pos(1, 0)
            if last_input == 'q':   delta = Pos(0, -1)
            elif last_input == 'd': delta = Pos(0, 1)
            if delta and s.map_handler.move_entity_relative(s.map_handler.player_pos, delta):
                s.map_handler.player_pos += delta
