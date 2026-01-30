from importlib.resources import path
import os
from typing import Iterable, Tuple, Optional
from termcolor import colored
from mazegen.generator import MazeGenerator, NORTH, SOUTH, EAST, WEST
import time


def clear():
    os.system("clear" if os.name == "posix" else "cls")


class ASCIIMazeRenderer:
    """ASCII Maze Renderer with colors and animation support."""

    WALL = "███"
    START = " S "
    END = " E "
    BLOCKED = "▓▓▓"
    VISITED = " . "
    FRONTIER = " ? "
    CURRENT = " @ "
    WALK = " * "
    PATH_MARKING = " X "

    def __init__(self, maze: MazeGenerator,
                 wall_color: str = "magenta",
                 start_color: str = "green",
                 end_color: str = "red",
                 path_color: str = "yellow",
                 visited_color: str = "cyan",
                 frontier_color: str = "blue",
                 current_color: str = "red",
                 blocked_color: str = "red",
                 background: Optional[str] = None):
        self.maze = maze
        self.wall_color = wall_color
        self.start_color = start_color
        self.end_color = end_color
        self.path_color = path_color
        self.visited_color = visited_color
        self.frontier_color = frontier_color
        self.current_color = current_color
        self.blocked_color = blocked_color
        self.background = background

    def render(self,
               walk: Optional[Iterable[Tuple[int, int]]] = None,
               visited: Optional[Iterable[Tuple[int, int]]] = None,
               frontier: Optional[Iterable[Tuple[int, int]]] = None,
               current: Optional[Tuple[int, int]] = None,
               walked_path: Optional[Iterable[Tuple[int, int]]] = None):
        walk = set(walk or [])
        visited = set(visited or [])
        frontier = set(frontier or [])
        walked_path = set(walked_path or [])
        clear()
        m = self.maze

        # Top border
        line: str = "+"
        for x in range(m.width):
            if (m.grid[0][x] & NORTH):
                line += colored("---+", self.wall_color,
                                on_color=self.background)
            else:
                line += colored("   +", None,
                                on_color=self.background
                                ) if self.background else "   +"
        print(line)

        for y in range(m.height):
            row: str = ""
            for x in range(m.width):
                cell = m.grid[y][x]

                # West wall
                if (cell & WEST):
                    row += colored("|", self.wall_color,
                                   on_color=self.background)
                else:
                    row += colored(" ", None,
                                   on_color=self.background
                                   ) if self.background else " "

                # Cell content
                if (x, y) in m.blocked:
                    row += colored(self.BLOCKED,
                                   self.blocked_color,
                                   on_color=self.background)
                elif (x, y) == m.start:
                    row += colored(self.START, self.start_color,
                                   on_color=self.background)
                elif (x, y) == m.end:
                    row += colored(self.END, self.end_color,
                                   on_color=self.background)
                elif (x, y) in walk:
                    row += colored(self.WALK, self.path_color,
                                   on_color=self.background)
                elif walked_path and (x, y) in walked_path:
                    symbol = self.PATH_MARKING
                    row += colored(symbol, self.path_color,
                                   on_color=self.background)
                elif current == (x, y):
                    row += colored(self.CURRENT,
                                   self.current_color,
                                   on_color=self.background)
                elif frontier and (x, y) in frontier:
                    row += colored(self.FRONTIER,
                                   self.frontier_color,
                                   on_color=self.background)
                elif visited and (x, y) in visited:
                    row += colored(self.VISITED,
                                   self.visited_color,
                                   on_color=self.background)
                else:
                    row += colored("   ", None,
                                   on_color=self.background
                                   ) if self.background else "   "

            # East wall of last cell
            if (m.grid[y][m.width - 1] & EAST):
                row += colored("|", self.wall_color, on_color=self.background)
            else:
                row += colored(" ", None,
                               on_color=self.background
                               ) if self.background else " "
            print(row)

            # South walls
            row = colored(
                "+", None, on_color=self.background
            ) if self.background else "+"
            for x in range(m.width):
                if (m.grid[y][x] & SOUTH):
                    row += colored("---+", self.wall_color,
                                   on_color=self.background)
                else:
                    row += colored("   +", None,
                                   on_color=self.background
                                   ) if self.background else "   +"
            print(row)

    def render_path_animated(self,
                             walked_path: Iterable[Tuple[int, int]],
                             delay: float = 0.1,
                             walk: Optional[Iterable[Tuple[int, int]]] = None,
                             visited: Optional[Iterable
                                               [Tuple[int, int]]] = None):
        """Render path step by step with animation."""
        path_list = list(walked_path)
        walk = set(walk or [])
        visited = set(visited or [])

        for i in range(len(path_list) + 1):
            current_path = path_list[:i]
            current_pos = path_list[i-1] if i > 0 else None

            self.render(
                walk=walk,
                visited=visited,
                current=current_pos,
                walked_path=current_path
            )

            if i < len(path_list):
                time.sleep(delay)
