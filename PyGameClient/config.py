from utils import Pos


DISPLAY_CONFIG = {
    'fps': 8,
    'target_resolution': Pos(x=1800, y=1000),
    'hud_width_px': 200,
    'tile_size': 32,
    'borders_width': 2,
}

MAP_CONFIG = {
    'map_size': 32,
    'chunk_size': 32,
    'seed': 0,
    'noise_scale': 5,
    'layouts': {
            'Corridors': {
                'proportion': 1,
                'room_probability': 10,
                'mean_room_size': 3,
                'avg_link_nbr': 90,
                'range_lower_value': 0,
                'range_upper_value': 0,
        },
            'Small rooms': {
                'proportion': 2,
                'room_probability': 50,
                'mean_room_size': 10,
                'avg_link_nbr': 50,
                'range_lower_value': 0,
                'range_upper_value': 0,
        },
            'Medium rooms': {
                'proportion': 2,
                'room_probability': 50,
                'mean_room_size': 20,
                'avg_link_nbr': 50,
                'range_lower_value': 0,
                'range_upper_value': 0,
        },
            'Big rooms': {
                'proportion': 3,
                'room_probability': 30,
                'mean_room_size': 30,
                'avg_link_nbr': 50,
                'range_lower_value': 0,
                'range_upper_value': 0,
        },
            'Boss': {
                'proportion': 6,
                'room_probability': 10,
                'mean_room_size': 60,
                'avg_link_nbr': 50,
                'range_lower_value': 0,
                'range_upper_value': 0,
        },
    },
}
