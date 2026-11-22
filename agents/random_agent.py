from .base_agent import BaseAgent


class RandomAgent(BaseAgent):

    def choose_shot(self):

        available_cells = self.get_available_cells()

        if not available_cells:
            raise RuntimeError("No available cells left.")

        return self.rng.choice(available_cells)

