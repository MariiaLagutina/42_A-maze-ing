import random
from typing import List, Tuple, Set
from mazegen.generator import MazeGenerator
from renderer.render import ASCIIMazeRenderer
import time


class BacktrackerGenerator(MazeGenerator):
    """
    Generates a maze using the Recursive Backtracker algorithm
    (iterative depth-first search).
    """

    def generate(self, delay: float = 0.02) -> None:
        self._draw_42()
        self.renderer: ASCIIMazeRenderer = ASCIIMazeRenderer(self)

        stack: List[Tuple[int, int]] = []
        visited: Set[Tuple[int, int]] = set()

        # Blocked cells (the "42" pattern) are treated as already visited
        visited.update(self.blocked)

        # Start position
        sx, sy = self.start
        stack.append((sx, sy))
        visited.add((sx, sy))

        # Possible movement directions (dx, dy)
        moves = [
            (0, -1),  # North
            (0, 1),   # South
            (1, 0),   # East
            (-1, 0)   # West
        ]

        while stack:
            cx, cy = stack[-1]
            unvisited_neighbors: List[Tuple[int, int]] = []
            for dx, dy in moves:
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
            self.renderer.render()
            time.sleep(delay)
