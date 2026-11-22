from agents.base_agent import BaseAgent
from agents.inference import (
    filter_compatible_configurations,
    calculate_probability_matrix
)
from game.configurations import generate_configurations


class MaximumProbabilityAgent(BaseAgent):

    def __init__(self, n, fleet_lengths, rng=None):

        super().__init__(n, rng)

        self.fleet_lengths = fleet_lengths

        self.configurations = generate_configurations(
            n,
            fleet_lengths
        )

        if not self.configurations:
            raise ValueError(
                "No legal fleet configurations available."
            )

    def choose_shot(self):

        available_cells = self.get_available_cells()

        if not available_cells:
            raise RuntimeError("No available cells left.")

        # 1. Keep only configurations compatible
        #    with the observations.
        compatible_configurations = (
            filter_compatible_configurations(
                self.configurations,
                self.observations
            )
        )

        if not compatible_configurations:
            raise RuntimeError(
                "No fleet configurations are compatible "
                "with the observations."
            )

        # 2. Calculate posterior occupancy probabilities.
        probability_matrix = calculate_probability_matrix(
            self.n,
            compatible_configurations
        )

        # 3. Find the maximum probability among
        #    cells that have not been attacked.
        max_probability = max(
            probability_matrix[row][col]
            for row, col in available_cells
        )

        best_cells = [
            (row, col)
            for row, col in available_cells
            if probability_matrix[row][col] == max_probability
        ]

        # 4. Break ties randomly.
        return self.rng.choice(best_cells)
