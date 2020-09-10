import time
import curses

from utils import Pos


class CliHandler(object):
    def __init__(s, stdscr, fps=20, hud_width=35):
        ### Check if terminal does support colors ###
        if not curses.has_colors() or not curses.can_change_color():
            exit_error("Display error: Colors not supported by terminal")
        curses.use_default_colors()
        s.color_pairs_dict = {}
        ### Prepare layout and display
        curses.curs_set(0)  # Disable cursor
        s.stdscr = stdscr
        s.screen_size = Pos(curses.LINES - 1, curses.COLS)
        ### Check if terminal is not too big, if so, restrict size ###
        if s.screen_size.y > 50 or s.screen_size.x > 240:
            s.screen_size = Pos(50, 240)
            print("Display warning: Terminal is too big, capping at 240 x 50")
        s.hud_width = hud_width
        s.hud_x_start = s.screen_size.x - 3 - hud_width
        s.map_scr = curses.newwin(
                            s.screen_size.y - 1,
                            # left: - 1 Space - 1 map border
                            # right: - 1 map border - hud_width - 1 border - 1 space
                            s.screen_size.x - 5 - hud_width,
                            1,
                            2
                    )
        s.map_screen_size = Pos(*s.map_scr.getmaxyx())
        s.hud_scr = curses.newwin(
                            s.screen_size.y - 1,
                            hud_width,
                            1,
                            s.hud_x_start + 1
                    )
        ### FPS related ###
        s.delta = 1 / fps
        s.frame_start = time.time()
        ### Inputs related ###
        s.stdscr.nodelay(True)
        ### Draw borders ###
        map_screen_width = s.map_scr.getmaxyx()[1]
        try:
            s.stdscr.addstr(0, 1, f"╔{'═' * map_screen_width}╦{'═' * s.hud_width}╗")
            for y in range(1, s.screen_size.y):
                s.stdscr.addstr(y, 1, '║')
                s.stdscr.addstr(y, 2 + map_screen_width, '║')
                s.stdscr.addstr(y, s.screen_size.x - 2, '║')
            s.stdscr.addstr(s.screen_size.y, 1, f"╚{'═' * map_screen_width}╩{'═' * s.hud_width}╝")
        except:
            pass
        s.stdscr.refresh()

    def draw(s, map_handler, info_list):
        s.draw_hud(info_list)
        s.draw_map(map_handler)
        s.handle_sleep()

    def draw_map(s, map_handler):
        # Nbr of lines available from the player (-1) to the top of the map screen
        needed_lines_top = s.map_screen_size.y // 2
        to_add_top = needed_lines_top - map_handler.player_pos.y
        term_y_idx = 0 if to_add_top <= 0 else to_add_top
        map_y_idx = 0 if to_add_top >= 0 else -to_add_top

        # Half the screen, and a square takes two chars so divide by 4
        needed_squares_left = s.map_screen_size.x // 4
        squares_to_add_left = needed_squares_left - map_handler.player_pos.x
        shift_x = 0 if squares_to_add_left <= 0 else squares_to_add_left
        shift_x *= 2  # Square to char
        map_x_start = 0 if squares_to_add_left >= 0 else -squares_to_add_left


        avail_squares_right = ((s.map_screen_size.x + 2) // 2) // 2
        map_x_end = map_handler.player_pos.x + avail_squares_right + 1

        # Prevent leaving "marks" of the previously drawn map at the top of the newly drawn map
        s.map_scr.move(max(0, term_y_idx - 1), 0)
        s.map_scr.clrtoeol()
        while term_y_idx < s.map_screen_size.y:
            s.map_scr.move(term_y_idx, 0)
            s.map_scr.clrtoeol()
            try:
                tmp_line = map_handler.map[map_y_idx][map_x_start:map_x_end]
            except IndexError:
                break
            for x_idx, square in enumerate(tmp_line):
                try:
                    if square:
                        color_pair_idx = s.get_color_pair_idx(square.get_colors())
                        s.map_scr.addstr(
                                    term_y_idx, shift_x + x_idx * 2,
                                    square.get_char(),
                                    curses.color_pair(color_pair_idx)
                                )
                    else:
                        s.map_scr.addstr(term_y_idx, shift_x + x_idx * 2, "  ")
                except curses.error:
                    pass  # Needed for last char of last line
            term_y_idx += 1
            map_y_idx += 1
        # Prevent leaving "marks" of the previously drawn map at the bottom of the newly drawn map
        try:
            s.map_scr.move(term_y_idx, 0)
            s.map_scr.clrtoeol()
        except curses.error:
            pass  # We try to erase the last line

        s.map_scr.refresh()

    def draw_hud(s, info_list):
        y_idx = 0
        for key, value in info_list.items():
            if key == "separator":
                s.hud_scr.addstr(y_idx, 0, '─'* s.hud_width)
            elif key == "empty":
                continue
            else:
                final_str = f" {key}: {value}" if value != None else f" {key}"
                s.hud_scr.addstr(y_idx, 0, final_str)
            y_idx += 1
        s.hud_scr.refresh()

    def get_color_pair_idx(s, color_pair):
        if color_pair in s.color_pairs_dict:
            return s.color_pairs_dict[color_pair]
        else:
            color_pair_idx = len(s.color_pairs_dict) + 1
            curses.init_pair(color_pair_idx, color_pair[0], color_pair[1])
            s.color_pairs_dict[color_pair] = color_pair_idx
            return color_pair_idx

    def get_inputs(s):
        keys = None
        try:
            keys = s.stdscr.getkey()
        except curses.error:
            pass
        curses.flushinp()
        return keys

    def handle_sleep(s):
        to_sleep = s.delta - (time.time() - s.frame_start)
        if to_sleep > 0:
            time.sleep(to_sleep)
        else:
            s.stdscr.addstr(s.screen_size.y, 20, f"Lagging {-to_sleep} seconds behind")
        s.frame_start = time.time()
