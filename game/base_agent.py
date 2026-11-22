
from abc import ABC, abstractmethod

from game.observation import GameObservation
from game.game_engine import ShotResult


class BaseAgent(ABC):

    @abstractmethod
    def choose_shot(
        self,
        observation: GameObservation
    ) -> tuple[int, int]:
        """
        Select the next cell to attack.
        """

        pass

    def observe(
        self,
        cell: tuple[int, int],
        result: ShotResult
    ) -> None:
        """
        Receive the result of a shot.

        Agents can override this method to update
        their internal state.
        """

        pass
