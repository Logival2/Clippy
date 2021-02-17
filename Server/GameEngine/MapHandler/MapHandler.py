from GameEngine.MapHandler.MapGenerator import MapGenerator
from GameEngine.Components import *


class MapHandler(object):
    def __init__(self, ecs):
        self.ecs = ecs
        self.map = {}
        self.map_generator = MapGenerator(ecs)
        self.loaded_chunks_anchors = []

    def add_chunk_to_map(self, chunk_to_be_loaded_anchor):
        if chunk_to_be_loaded_anchor in self.loaded_chunks_anchors:
            return  # Already loaded
        serialized = False
        # TODO: check if this chunk has been serialized
        if serialized:
            pass  # load it from the file
        else:  # create it
            new_chunk = self.map_generator.generate_chunk(chunk_to_be_loaded_anchor)
            # Now add the newly created chunk to the map object
            for y_idx, y_line_data in new_chunk.items():
                if y_idx not in self.map:
                    self.map[y_idx] = y_line_data
                else:
                    self.map[y_idx].update(y_line_data)
        self.loaded_chunks_anchors.append(chunk_to_be_loaded_anchor)

    def remove_chunk_from_map(self, chunk_to_be_deleted_anchor):
        if chunk_to_be_deleted_anchor not in self.loaded_chunks_anchors:
            return  # Not loaded
        # Remove it from self.map AND KEEP IT (for serialization)
        tmp_chunk = {}
        chunk_end = chunk_to_be_deleted_anchor + self.map_generator.config['chunk_size']
        for y_idx in range(chunk_to_be_deleted_anchor.y, chunk_end.y):
            tmp_chunk[y_idx] = {}
            for x_idx in range(chunk_to_be_deleted_anchor.x, chunk_end.x):
                tmp_chunk[y_idx][x_idx] = self.map[y_idx].pop(x_idx)
        # Remove it from the list of loaded chunks anchors
        self.loaded_chunks_anchors.remove(chunk_to_be_deleted_anchor)
        # Now write it to file

        # Write ids and components to file
        # Remove ID from ecs
        to_delete = []
        chunk_size = self.map_generator.config['chunk_size']
        for k, v in self.ecs.game_state["components"]["Position"].items():
            player_pos = v
            player_chunk_anchor = (player_pos // chunk_size) * chunk_size
            if player_chunk_anchor == chunk_to_be_deleted_anchor:
                to_delete.append(k)
        for id in to_delete:
            self.ecs.delete_id(id)


    def handle_chunks(self):
        to_be_loaded_chunk_anchors = []
        # Handle chunk loading
        for player_id, player_data in self.ecs.game_state["players"].items():
            player_entity_id = player_data["entity_id"]
            player_pos = self.ecs.game_state["components"]["Position"][player_entity_id]
            chunk_size = self.map_generator.config['chunk_size']
            player_chunk_anchor = (player_pos // chunk_size) * chunk_size
            to_be_loaded_chunk_anchors = self.get_neighbours_chunk_anchors(
                player_chunk_anchor, chunk_size
            )
        for chunk_to_be_loaded_anchor in to_be_loaded_chunk_anchors:
            self.add_chunk_to_map(chunk_to_be_loaded_anchor)
        # Handle chunk deloading by removing all the chunks
        # whose anchor is in self.loaded_chunks_anchors but not in
        # to_be_loaded_chunk_anchors
        for loaded_chunk_anchor in self.loaded_chunks_anchors:
            if loaded_chunk_anchor not in to_be_loaded_chunk_anchors:
                self.remove_chunk_from_map(loaded_chunk_anchor)

    def get_neighbours_chunk_anchors(self, anchor, chunk_size):
        tmp_pos = Position.Position(chunk_size, chunk_size)
        return [
            # Current chunk
            anchor,
            # Top
            Position.Position(
                x=anchor.x,
                y=anchor.y - chunk_size,
            ),
            # Bottom
            Position.Position(
                x=anchor.x,
                y=anchor.y + chunk_size,
            ),
            # Left
            Position.Position(
                x=anchor.x - chunk_size,
                y=anchor.y,
            ),
            # Right
            Position.Position(
                x=anchor.x + chunk_size,
                y=anchor.y,
            ),
            # Top left
            anchor - tmp_pos,
            # Bottom Right
            anchor + tmp_pos,
            # Top right
            Position.Position(
                x=anchor.x + chunk_size,
                y=anchor.y - chunk_size,
            ),
            # Bottom Left
            Position.Position(
                x=anchor.x - chunk_size,
                y=anchor.y + chunk_size,
            ),
        ]
