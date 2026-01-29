import os
from typing import Iterable, Tuple
from mazegen.generator import (
    NORTH, SOUTH, EAST, WEST, MazeGenerator
)


def clear():
    os.system("clear" if os.name == "posix" else "cls")


class ASCIIMazeRenderer:
    def __init__(self, maze: MazeGenerator):
        self.maze = maze

    def render(self, walk: Iterable[Tuple[int, int]] | None = None,
               visited=None,
               frontier=None,
               current=None,
               path=None):
        clear()
        m = self.maze
        walk = set(walk) if walk else set()

        # Top border
        line = "+"
        for x in range(m.width):
            line += "---+" if (m.grid[0][x] & NORTH) else "   +"
        print(line)

        for y in range(m.height):
            # Cell row
            row = ""
            for x in range(m.width):
                cell = m.grid[y][x]

                # West wall
                row += "|" if (cell & WEST) else " "

                # Cell content
                if (x, y) in m.blocked:
                    row += "███"
                elif (x, y) == m.start:
                    row += " S "
                elif (x, y) == m.end:
                    row += " E "
                elif (x, y) in walk:
                    row += " * "
                elif path and (x, y) in path:
                    row += " o "
                elif current == (x, y):
                    row += " @ "
                elif frontier and (x, y) in frontier:
                    row += " ? "
                elif visited and (x, y) in visited:
                    row += " . "
                else:
                    row += "   "

            # East wall of last cell
            row += "|" if (m.grid[y][m.width - 1] & EAST) else " "
            print(row)

            # South walls
            row = "+"
            for x in range(m.width):
                row += "---+" if (m.grid[y][x] & SOUTH) else "   +"
            print(row)


def rest():
    print("rest")