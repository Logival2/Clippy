import random
import math


def generate_voronoi(width, height, values):
    values += values
    nx, ny = [], []
    # Init map
    map = []
    for y in range(height):
        map.append([' '] * width)
    # Define each region main point
    for c in values:
        point_x = random.randint(0, width)
        while point_x < 0 or point_x >= width:
            point_x = random.randint(0, width)
        point_y = random.randint(0, height)
        while point_y < 0 or point_y >= height:
            point_y = random.randint(0, height)
        nx.append(point_x)
        ny.append(point_y)
    # Compute diagram
    for y in range(height):
        for x in range(width):
            dmin = math.hypot(width - 1, height - 1)
            j = -1
            for i in range(len(values)):
                d = math.hypot(nx[i] - x, ny[i] - y)
                if d < dmin:
                    dmin = d
                    j = i
            map[y][x] = values[j]
    # Add the main points (debug)
    # for i in range(len(values)):
    #     map[ny[i]][nx[i]] = 'p'
    return map


if __name__ == '__main__':
    map = generate_voronoi(width=200, height=45, values=['⠐', '⠸', '⠗', '⣗', '⣿'])
    for line in map:
        print(''.join(line))
