from GameEngine.Components.Position import Position


def get_neighbours_chunk_anchors(anchor, chunk_size):
    tmp_pos = Position(chunk_size, chunk_size)
    return [
        # Current chunk
        anchor,
        # Top
        Position(
            x=anchor.x,
            y=anchor.y - chunk_size,
        ),
        # Bottom
        Position(
            x=anchor.x,
            y=anchor.y + chunk_size,
        ),
        # Left
        Position(
            x=anchor.x - chunk_size,
            y=anchor.y,
        ),
        # Right
        Position(
            x=anchor.x + chunk_size,
            y=anchor.y,
        ),
        # Top left
        anchor - tmp_pos,
        # Bottom Right
        anchor + tmp_pos,
        # Top right
        Position(
            x=anchor.x + chunk_size,
            y=anchor.y - chunk_size,
        ),
        # Bottom Left
        Position(
            x=anchor.x - chunk_size,
            y=anchor.y + chunk_size,
        ),
    ]
