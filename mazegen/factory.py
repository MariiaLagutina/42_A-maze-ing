from typing import Optional
from .generator import MazeGenerator
from .backtracker import BacktrackerGenerator
from .wilson import WilsonGenerator
from enum import Enum


class _GENERATORS(Enum):
    backtracker = BacktrackerGenerator
    wilson = WilsonGenerator


class MazeFactory:
    @staticmethod
    def get_maze_generator(
        algorithm: str,
        width: int,
        height: int,
        seed: Optional[int] = None
    ) -> MazeGenerator:
        """
        Factory function to return the correct maze generator instance.

        Args:
            algorithm: Name of the algorithm ('backtracker' or 'wilson').
            width: Maze width.
            height: Maze height.
            seed: Random seed for reproducibility.
        """
        # Mapping between algorithm names and their generator classes

        algorithm = algorithm.lower().strip()

        try:
            generator_cls = _GENERATORS[algorithm].value
        except KeyError:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        return generator_cls(width, height, seed)
