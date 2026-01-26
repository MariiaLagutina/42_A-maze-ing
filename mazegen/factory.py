from typing import Optional, Type, Dict
from .generator import MazeGenerator
from .backtracker import BacktrackerGenerator
from .wilson import WilsonGenerator


# Mapping between algorithm names and their generator classes
_GENERATORS: Dict[str, Type[MazeGenerator]] = {
    "backtracker": BacktrackerGenerator,
    "wilson": WilsonGenerator,
}


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
    algorithm = algorithm.lower().strip()

    try:
        generator_cls = _GENERATORS[algorithm]
    except KeyError:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    return generator_cls(width, height, seed)
