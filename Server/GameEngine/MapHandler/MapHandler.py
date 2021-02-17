from GameEngine.utils import *
from GameEngine.MapHandler.MapGenerator import MapGenerator


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
            pass
        else:  # create it
            print("creating chunk", chunk_to_be_loaded_anchor)
            new_chunk = self.map_generator.generate_chunk(chunk_to_be_loaded_anchor)
            # Now add the newly created chunk to the map object
            for y_idx, y_line_data in new_chunk.items():
                if y_idx not in self.map:
                    self.map[y_idx] = y_line_data
                else:
                    self.map[y_idx].update(y_line_data)
            self.loaded_chunks_anchors.append(chunk_to_be_loaded_anchor)

    def remove_chunk_from_map(self, chunk_to_be_deleted_anchor):
        # self.loaded_chunks_anchors.remove(chunk_to_be_deleted_anchor)
        # Now remove from self.map as well
        pass

    def handle_chunks(self):
        to_be_loaded_chunk_anchors = []
        # Handle chunk loading
        for player_id, player_data in self.ecs.game_state["players"].items():
            player_entity_id = player_data["entity_id"]
            player_pos = self.ecs.game_state["components"]["Position"][player_entity_id]
            chunk_size = self.map_generator.config['chunk_size']
            player_chunk_anchor = (player_pos // chunk_size) * chunk_size
            to_be_loaded_chunk_anchors = get_neighbours_chunk_anchors(
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
