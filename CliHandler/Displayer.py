def display_map(map_handler, term_layout):
    cropped_map = crop_map(map_handler, term_layout)
    print(f"\033[K\033[1;2H╔{'═'*(term_layout.info_column_pos - 2)}", end='')
    map_end = 0
    for y, l in enumerate(map_handler.map):
            # \033[K erase line, then print
            print(f"\033[K\033[{y + 2};2H║ ", end='')
            for entity in l:
                if entity:
                    repr = entity.__repr__()
                    print(repr * 2, end='')
                else:
                    print("  ", end='')
            map_end = y
    for i in range(map_end, term_layout.end_y_idx):
        print(f"\033[K\033[{i};2H║", end='')
    print(f"\033[K\033[{term_layout.end_y_idx};2H╚{'═'*(term_layout.info_column_pos - 2)}", end='')

def crop_map(map_handler, term_layout):
    pass
