"""
Goal is to process all the rotated sprites and add a few semi transparent pixels
around them, to create a smoother display
The ingame tiles won't change size, but the textures will overlap and blend
"""
import os
import copy
from pprint import pprint
import glob
import random

import png


OUTPUT_DIR = "GameEngine/Displayer/upscaled_assets/"

def process_sprite(sprite, empty_borders, border_ratio):
    # I assume all sprite are square, as I created em
    image_width = sprite[0]
    border_size = image_width // border_ratio
    final_size = image_width + (2 * border_size)
    # Create a new, bigger png, to contain the image
    # and its new semi transparent borders
    new_sprite = png.Writer(
        size=(final_size, final_size),
        greyscale=sprite[3]["greyscale"],
        alpha=sprite[3]["alpha"],
        bitdepth=sprite[3]["bitdepth"],
    )
    #####
    # Transform the png object into a list of lists
    # And save all pixels within {border_size} pixels of the border
    # in borders pixel, so we can use them randomly before to create
    # the extended borders
    #####
    res = []
    borders_pixels = []
    for idx, line in enumerate(sprite[2]):
        # Convert bytes to list
        tmp_list = [v for v in line]
        # split it into list of each pixel (R, G, B, A) values
        pixel_list = [tmp_list[i:i + 4] for i in range(0, len(tmp_list), 4)]
        if idx < border_size or idx > final_size - border_size:
            borders_pixels += pixel_list
        else:
            borders_pixels += pixel_list[:border_size]
            borders_pixels += pixel_list[-border_size:]
        res.append(tmp_list)
    if empty_borders:
        borders_pixels = [[0, 0, 0, 0]]
    #####
    # Now add the pixels needed for the extended borders
    #####
    # Add left and right borders
    for idx, line in enumerate(res):
        line_start = [random.choice(borders_pixels) for i in range(border_size)]
        flat_line_start = [item for sublist in line_start for item in sublist]
        line_end = [random.choice(borders_pixels) for i in range(border_size)]
        flat_line_end = [item for sublist in line_end for item in sublist]
        res[idx] = flat_line_start + res[idx] + flat_line_end
    # create top lines
    for i in range(border_size):
        new_line = [random.choice(borders_pixels) for i in range(final_size)]
        flat_new_line = [item for sublist in new_line for item in sublist]
        res.insert(0, flat_new_line)
    # create bottom lines
    for i in range(border_size):
        new_line = [random.choice(borders_pixels) for i in range(final_size)]
        res.append([item for sublist in new_line for item in sublist])

    if empty_borders:
        return new_sprite, res
    #####
    # Now decrease alpha value for the pixels in the extended border
    #####
    pixel_alpha_step = 255 // border_size
    # Lateral borders
    for y_idx, line in enumerate(res):
        # Left border
        for x_idx, pixel_alpha_value_idx in enumerate(range(3, border_size * 4, 4)):
            res[y_idx][pixel_alpha_value_idx] = random.randint(0, 255)
        # Right border
        for x_idx, pixel_alpha_value_idx in enumerate(range((final_size * 4) - (border_size * 4) + 3, (final_size * 4), 4)):
            res[y_idx][pixel_alpha_value_idx] = random.randint(0, 255)
    # Top lines
    for y_idx in range(border_size):
        for x_idx, pixel_alpha_value_idx in enumerate(range(3, final_size * 4, 4)):
            res[y_idx][pixel_alpha_value_idx] = random.randint(0, 255)
    # Top lines
    for y_idx in range(final_size - border_size, final_size):
        for x_idx, pixel_alpha_value_idx in enumerate(range(3, final_size * 4, 4)):
            res[y_idx][pixel_alpha_value_idx] = random.randint(0, 255)
    return new_sprite, res


def upscale_sprites(border_ratio, folder_path, empty_borders, output_path):
    # Do border drawing sprites
    files = [f for f in glob.glob(folder_path + "**/*.png", recursive=False)]
    for filepath in files:
        print("Processing", filepath)
        new_sprite, res = process_sprite(
            png.Reader(filename=filepath).read(),
            empty_borders,
            border_ratio,
        )
        filename = filepath[filepath.rfind('/') + 1:]
        # Create output_path if it does not exist
        try:
            os.mkdir(output_path)
        except:
            pass
        with open(os.path.join(output_path, filename), 'wb') as fd:
            new_sprite.write(fd, res)
