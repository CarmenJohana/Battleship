from agents.base_agent import BaseAgent
from agents.inference import (
    filter_compatible_configurations,
    calculate_information_gain
)
from game.configurations import generate_configurations


class MaximumInformationGainAgent(BaseAgent):

    def __init__(self, n, fleet_lengths, rng=None):
        super().__init__(n, rng)

        self.fleet_lengths = fleet_lengths
        self.configurations = generate_configurations(
            n, fleet_lengths
        )

        if not self.configurations:
            raise ValueError(
                "No legal fleet configurations available."
            )

        
    def choose_shot(self):
        available_cells = self.get_available_cells()

        if not available_cells:
            raise RuntimeError("No available cells left.")

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

        information_gains = {
            cell: calculate_information_gain(
                compatible_configurations,
                cell
            )
            for cell in available_cells
        }

        max_information_gain = max(
            information_gains.values()
        )

        best_cells = [
            cell
            for cell, gain in information_gains.items()
            if abs(gain - max_information_gain) < 1e-12
        ]

        return self.rng.choice(best_cells)
