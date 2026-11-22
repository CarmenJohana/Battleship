
from .game_engine import ShotResult


class GameRunner:

    def __init__(self, engine, agent):

        if engine.n != agent.n:
            raise ValueError(
                "Engine and agent must use the same board size."
            )

        self.engine = engine
        self.agent = agent

        self.history = []

    def run(self):

        while not self.engine.is_over:

            # The agent selects a cell.
            cell = self.agent.choose_shot()

            # The engine evaluates the shot.
            result = self.engine.fire(cell)

            # An invalid shot indicates an agent or synchronization error.
            if result == ShotResult.INVALID:
                raise RuntimeError(
                    f"Agent selected an invalid shot: {cell}"
                )

            # The agent receives only the shot result.
            self.agent.observe(cell, result)

            # Save the event.
            self.history.append((cell, result))

        return self.history
