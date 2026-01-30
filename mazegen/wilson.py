import random
from typing import List, Tuple, Set
from mazegen.generator import MazeGenerator
import time
from renderer.render import ASCIIMazeRenderer


class WilsonGenerator(MazeGenerator):
    """
    Generates a maze using Wilson's Algorithm.
    This creates a Uniform Spanning Tree (UST), meaning all possible mazes
    have exactly the same probability of being generated.
    """

    def generate(self, delay: float = 0.02) -> None:
        self._draw_42()
        self.renderer = ASCIIMazeRenderer(self)
        # Cells already in the maze
        visited: Set[Tuple[int, int]] = set()
        visited.update(self.blocked)

        # Cells not yet in the maze
        unvisited: List[Tuple[int, int]] = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in visited
        ]

        if not unvisited:
            return

        # Seed the maze with one random cell
        first_cell = random.choice(unvisited)
        unvisited.remove(first_cell)
        visited.add(first_cell)

        # Main Wilson loop
        while unvisited:
            start = random.choice(unvisited)

            # Loop-erased random walk stored as an ordered list
            walk: List[Tuple[int, int]] = [start]
            current = start

            while current not in visited:
                neighbors: List[Tuple[int, int]] = []
                for dx, dy in self.possible_moves:
                    nx, ny = current[0] + dx, current[1] + dy
                    if (
                        0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) not in self.blocked
                    ):
                        neighbors.append((nx, ny))

                next_cell = random.choice(neighbors)

                # Proper loop erasing:
                if next_cell in walk:
                    idx = walk.index(next_cell)
                    walk = walk[:idx + 1]
                else:
                    walk.append(next_cell)
                self.renderer.render(walk)
                time.sleep(delay)
                current = next_cell

            # Carve the loop-erased path into the maze
            for i in range(len(walk) - 1):
                x1, y1 = walk[i]
                x2, y2 = walk[i + 1]

                self._remove_wall(x1, y1, x2, y2)

                visited.add((x1, y1))
                unvisited.remove((x1, y1))
                self.renderer.render()
                time.sleep(delay)
