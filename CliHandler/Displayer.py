def display_map(map):
    for y, l in enumerate(map):
            # \033[K erase line, then print
            print(f"\033[K\033[{y + 1};1H", end='')
            for entity in l:
                if entity:
                    repr = entity.__repr__()
                    print(repr * 2, end='')
                else:
                    print("  ", end='')
    print(f"\033[{len(map) + 1};1H")  # Reset cursor
