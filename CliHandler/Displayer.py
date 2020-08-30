def display_map(scaling_factor, map):
    line_idx = 1
    for l in map:
        for _ in range(scaling_factor.y):
            # \033[K erase line, then print
            print(f"\033[K\033[{line_idx};1H", end='')
            line_idx += 1
            for entity in l:
                if entity:
                    repr = entity.__repr__()
                    print(repr * scaling_factor.x, end='')
                else:
                    print(" " * scaling_factor.x, end='')
    print(f"\033[{len(map) * scaling_factor.y + 1};1H")  # Reset cursor
