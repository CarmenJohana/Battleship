def generate_placements(n: int, length: int) -> list[tuple[tuple[int, int], ...]]:
    """
    Generate all possible horizontal and vertical placements
    for a straight ship on an n x n board.

    Coordinates use zero-based indexing.

    A placement is represented as a tuple of cells:
        ((row_1, col_1), (row_2, col_2), ...)
    """

    if n <= 0:
        raise ValueError("Board size must be positive.")

    if length <= 0:
        raise ValueError("Ship length must be positive.")

    if length > n:
        return []

    placements = []

    # Horizontal placements
    for row in range(n):
        for col in range(n - length + 1):
            cells = tuple(
                (row, col + offset)
                for offset in range(length)
            )
            placements.append(cells)

    # Vertical placements
    # A ship of length 1 has no distinct orientation.
    if length > 1:
        for row in range(n - length + 1):
            for col in range(n):
                cells = tuple(
                    (row + offset, col)
                    for offset in range(length)
                )
                placements.append(cells)

    return placements

