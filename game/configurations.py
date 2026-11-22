from .placements import generate_placements


def generate_configurations(
    n: int,
    fleet_lengths: list[int]
) -> list[tuple[tuple[tuple[int, int], ...], ...]]:

    if n <= 0:
        raise ValueError("Board size must be positive.")

    if any(length <= 0 for length in fleet_lengths):
        raise ValueError("Ship lengths must be positive.")

    if any(length > n for length in fleet_lengths):
        return []

    # Sort ships from longest to shortest.
    lengths = sorted(fleet_lengths, reverse=True)

    # Generate placements for each distinct ship length.
    placements_by_length = {
        length: generate_placements(n, length)
        for length in set(lengths)
    }

    configurations = []

    def backtrack(
        index: int,
        occupied: set[tuple[int, int]],
        chosen: list[tuple[tuple[int, int], ...]],
        last_indices: dict[int, int]
    ) -> None:

        # All ships have been placed.
        if index == len(lengths):
            configurations.append(tuple(chosen))
            return

        length = lengths[index]
        placements = placements_by_length[length]

        # Avoid permutations of identical ships.
        start = last_indices.get(length, -1) + 1

        for p_index in range(start, len(placements)):

            placement = placements[p_index]
            placement_cells = set(placement)

            # Reject overlapping placements.
            if not occupied.isdisjoint(placement_cells):
                continue

            previous_index = last_indices.get(length)

            # Choose this placement.
            chosen.append(placement)
            last_indices[length] = p_index

            # Explore the next ship.
            backtrack(
                index + 1,
                occupied | placement_cells,
                chosen,
                last_indices
            )

            # Backtrack: undo the choice.
            chosen.pop()

            if previous_index is None:
                del last_indices[length]
            else:
                last_indices[length] = previous_index

    backtrack(
        index=0,
        occupied=set(),
        chosen=[],
        last_indices={}
    )

    return configurations
