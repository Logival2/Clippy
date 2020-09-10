import json
import time

from opensimplex import OpenSimplex

from utils import Pos
from Entities import Square


class MapGenerator(object):
    """
    Holds the OpenSimplex instance and generates the map regions with get_region()
    noise_scale: bigger = "zoom out"
    the seed parameter is used for the simplex noise
    and the placement of items and entities
    """
    def __init__(s, noise_scale, seed=0):
        s.noise_scale = noise_scale
        s.simplex = OpenSimplex(seed)
        # Load biomes configuration files
        with open("./MapGenerator/biomes.json", 'r') as f:
            s.biomes = json.loads(f.read())
        # Create biome float values range to convert simplex noise float values to specific biomes
        s.compute_biome_values_ranges()

    def get_region(s, anchor, scale):
        """ Build and return the region (double array of Square objects)
        defined by the anchor (top left position)"""
        region_biomes = s.get_region_biomes(anchor, scale)
        s.print_y(region_biomes)
        region_squares_map = s.create_terrain(region_biomes)
        # region_squares_map = s.create_entities(region_squares_map)

    def create_terrain(s, region_biomes):
        rooms = []
        counts = []
        for line in region_biomes:
            for x in line:
                pass


    def print_y(s, region_biomes):
        for line in region_biomes:
            for biome_name in line:
                color_code = s.biomes[biome_name]["color"]
                print(f"""\x1b[30;48;5;{color_code}m{biome_name[0]*3}\x1b[0m""", end='')
            print()

    def get_region_biomes(s, anchor, scale):
        region_biomes = []
        for y in range(scale.y):
            tmp_line = []
            for x in range(scale.x):
                value = s.simplex.noise2d(y=(anchor.y + y) / s.noise_scale,
                                          x=(anchor.x + x) / s.noise_scale
                                  ) + 1  # In order to get values between 0 and 2
                for b_name, b_data in s.biomes.items():
                    if b_data["range_lower_value"] < value < b_data["range_upper_value"]:
                        tmp_line.append(b_name)
            region_biomes.append(tmp_line)
        return region_biomes

    def compute_biome_values_ranges(s):
        """ Define each range of float values in [0;2] to a specific biome,
        according to the proportions specified in s.biomes[0].
        the higher value of this range will be stored in s.biomes[3] """
        # Noise values range from 0 to 2, divide 2 by the total number
        # of sections to get a single gap value
        total = sum([b_data["proportion"] for _, b_data in s.biomes.items()])
        single_gap = 2 / total
        range_lower_value = 0
        for b_name, b_data in s.biomes.items():
            s.biomes[b_name]["range_lower_value"] = range_lower_value
            s.biomes[b_name]["range_upper_value"] = range_lower_value + (b_data["proportion"] * single_gap)
            range_lower_value = s.biomes[b_name]["range_upper_value"]


if __name__ == '__main__':
    mg = MapGenerator(noise_scale=200)
    region_size = Pos(40, 30)
    x_idx = 0
    # for x_idx in range(0, 1000, 15):
    print("\033[2J \033[0;0H")
    region_anchor = Pos(0, x_idx)
    mg.get_region(region_anchor, region_size)
    time.sleep(0.5)
