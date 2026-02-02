import random
from typing import List, Tuple, Set, Optional
from .generator import MazeGenerator, MazeRenderer
import time


class BacktrackerGenerator(MazeGenerator):
    """
    Generates a maze using the Recursive Backtracker algorithm
    (iterative depth-first search).
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        renderer: Optional[MazeRenderer] = None,
    ) -> None:
        super().__init__(width, height, seed)
        self.renderer: Optional[MazeRenderer] = renderer

    def generate(self, delay: float = 0.02,
                 renderer: Optional[MazeRenderer] = None) -> None:
        self._draw_42()
        if renderer is not None:
            self.renderer = renderer

        stack: List[Tuple[int, int]] = []
        visited: Set[Tuple[int, int]] = set()

        # Blocked cells (the "42" pattern) are treated as already visited
        visited.update(self.blocked)

        # Start position
        sx: int
        sy: int
        cx: int
        cy: int
        nx: int
        ny: int
        sx, sy = self.start
        stack.append((sx, sy))
        visited.add((sx, sy))

        while stack:
            cx, cy = stack[-1]
            unvisited_neighbors: List[Tuple[int, int]] = []
            for dx, dy in self.possible_moves:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        unvisited_neighbors.append((nx, ny))

            if unvisited_neighbors:
                nx, ny = random.choice(unvisited_neighbors)

                # Break wall between current cell and chosen neighbor
                self._remove_wall(cx, cy, nx, ny)

                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                # Backtrack
                stack.pop()
            if self.renderer is not None:
                self.renderer.render()
                time.sleep(delay)
