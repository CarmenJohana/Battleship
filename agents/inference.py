import math

from game.game_engine import ShotResult


def is_compatible(configuration, observations):
    """
    Check whether a fleet configuration is compatible
    with the agent's observations.
    """

    hit_cells = {
        cell
        for cell, result in observations.items()
        if result in (ShotResult.HIT, ShotResult.SUNK)
    }

    miss_cells = {
        cell
        for cell, result in observations.items()
        if result == ShotResult.MISS
    }

    sunk_cells = {
        cell
        for cell, result in observations.items()
        if result == ShotResult.SUNK
    }

    occupied_cells = {
        cell
        for placement in configuration
        for cell in placement
    }

    # Rule 1: no ship can occupy a missed cell.
    if not miss_cells.isdisjoint(occupied_cells):
        return False

    # Rule 2: every hit must correspond to an occupied cell.
    if not hit_cells.issubset(occupied_cells):
        return False

    # Rule 3: a sunk ship must be completely hit.
    for sunk_cell in sunk_cells:

        sunk_ship_found = False

        for placement in configuration:

            if sunk_cell in placement:

                sunk_ship_found = True

                if not set(placement).issubset(hit_cells):
                    return False

                break

        if not sunk_ship_found:
            return False

    return True


def filter_compatible_configurations(
    configurations,
    observations
):
    """
    Return only configurations compatible with observations.
    """

    return [
        configuration
        for configuration in configurations
        if is_compatible(configuration, observations)
    ]

def calculate_probability_matrix(n, configurations):
    """
    Calculate the posterior probability that each cell
    contains a ship, assuming a uniform prior over
    compatible configurations.
    """

    if n <= 0:
        raise ValueError("Board size must be positive.")

    if not configurations:
        raise ValueError(
            "Cannot calculate probabilities without configurations."
        )

    # Count how many configurations occupy each cell.
    occupancy_counts = [
        [0 for _ in range(n)]
        for _ in range(n)
    ]

    for configuration in configurations:

        occupied_cells = {
            cell
            for placement in configuration
            for cell in placement
        }

        for row, col in occupied_cells:

            if not (0 <= row < n and 0 <= col < n):
                raise ValueError(
                    "Configuration contains a cell outside the board."
                )

            occupancy_counts[row][col] += 1

    # Convert counts into probabilities.
    total_configurations = len(configurations)

    probability_matrix = [
        [
            occupancy_counts[row][col] / total_configurations
            for col in range(n)
        ]
        for row in range(n)
    ]

    return probability_matrix


def print_probability_matrix(probability_matrix):

    n = len(probability_matrix)

    print("Probability map")
    print("-" * (8 * n + 4))

    print("     " + "".join(
        f"{col:^8}"
        for col in range(n)
    ))

    for row in range(n):

        values = "".join(
            f"{probability_matrix[row][col]:^8.2f}"
            for col in range(n)
        )

        print(f"{row:>3}  {values}")

def calculate_information_gain(configurations, cell):
    """
    Calculate the expected information gain of shooting at a cell.

    Args:
        configurations: Compatible fleet configurations.
        cell: Candidate cell represented as (row, col).

    Returns:
        Expected information gain in bits.
    """
    if not configurations:
        raise ValueError("No compatible configurations available.")

    total_configurations = len(configurations)

    hit_count = 0

    for configuration in configurations:
        occupied_cells = {
            position
            for placement in configuration
            for position in placement
        }

        if cell in occupied_cells:
            hit_count += 1

    miss_count = total_configurations - hit_count

    hit_probability = hit_count / total_configurations
    miss_probability = miss_count / total_configurations

    information_gain = 0.0

    if hit_probability > 0:
        information_gain -= (
            hit_probability * math.log2(hit_probability)
        )

    if miss_probability > 0:
        information_gain -= (
            miss_probability * math.log2(miss_probability)
        )

    return information_gain
