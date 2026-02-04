import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Set, Protocol, Iterable, Dict, Any
from collections import deque
from enum import IntEnum


class Direction(IntEnum):
    """Bitwise wall representation for maze directions."""
    NORTH = 0b0001  # 1
    EAST = 0b0010   # 2
    SOUTH = 0b0100  # 4
    WEST = 0b1000   # 8
    ALL_WALLS = 0b1111  # 15 (0xF)

    @classmethod
    def opposite(cls, direction: 'Direction') -> 'Direction':
        """Get the opposite direction."""
        opposites = {
            cls.NORTH: cls.SOUTH,
            cls.SOUTH: cls.NORTH,
            cls.EAST: cls.WEST,
            cls.WEST: cls.EAST
        }
        return opposites[direction]


class MazeRenderer(Protocol):
    """Renderer protocol used by maze generators (Strategy pattern)."""

    def render(
        self,
        walk: Optional[Iterable[Tuple[int, int]]] = None,
        visited: Optional[Iterable[Tuple[int, int]]] = None,
        frontier: Optional[Iterable[Tuple[int, int]]] = None,
        current: Optional[Tuple[int, int]] = None,
        walked_path: Optional[Iterable[Tuple[int, int]]] = None,
        arrow: Optional[str] = None,
        path_directions: Optional[Dict[Any, Any]] = None
    ) -> None:
        ...

    def render_path_animated(self,
                             walked_path: Iterable[Tuple[int, int]],
                             delay: float = 0.1,
                             walk: Optional[Iterable[Tuple[int, int]]] = None,
                             visited: Optional[Iterable[Tuple[int, int]]]
                             = None
                             ) -> None:
        ...


class MazeGenerator(ABC):
    """
    Abstract Base Class for Maze Generators.

    Implements the Template Method pattern: shared logic (init, solving,
    drawing pattern) is here; specific generation logic is in child classes.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.message_42: str = ""
        if seed is not None:
            random.seed(seed)

        # Initialize grid: all cells start with all walls closed
        self.grid: List[List[int]] = [
            [Direction.ALL_WALLS for _ in range(width)] for _ in range(height)
        ]

        self.start: Tuple[int, int] = (0, 0)
        self.end: Tuple[int, int] = (width - 1, height - 1)

        # Permanently blocked cells (the "42" pattern)
        self.blocked: Set[Tuple[int, int]] = set()
        self.solution_path: Optional[str] = None
        self.solution_cells: Optional[List[Tuple[int, int]]] = None

        # Minimal size required to draw the "42" pattern safely
        self.min_width_42: int = 11
        self.min_height_42: int = 9
        # Possible movement directions (dx, dy)
        self.possible_moves: List[Tuple[int, int]] = [
            (0, -1),  # North
            (0, 1),   # South
            (1, 0),   # East
            (-1, 0)   # West
        ]

    def _draw_42(self) -> None:
        """
        Draws the '42' pattern centered in the grid by adding coordinates
        to the blocked set. Blocked cells remain fully closed.
        """
        if self.width < self.min_width_42 or self.height < self.min_height_42:
            self.message_42 = str("Info: Maze too small for '42'"
                                  " pattern. So it won't be drawn.")
            return
        digit_4 = [
            (-4, -2), (-2, -2), (-4, -1), (-2, -1), (-4, 0),
            (-3, 0), (-2, 0), (-2, 1), (-2, 2)
        ]

        digit_2 = [
            (1, -2), (2, -2), (3, -2), (3, -1), (1, 0), (2, 0),
            (3, 0), (1, 1), (1, 2), (2, 2), (3, 2)
        ]

        if self.width == 11:
            digit_4 = [(x + 1, y) for x, y in digit_4]

        cx, cy = self.width // 2, self.height // 2

        for dx, dy in digit_4 + digit_2:
            x, y = cx + dx, cy + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.blocked.add((x, y))
        # Validate that start and end points are not blocked
        self._validate_start_end_points()

    def _validate_start_end_points(self) -> None:
        """
        Validates that start and end points are not blocked cells.
        Raises ValueError if either is blocked (invalid input).
        """
        if self.start in self.blocked:
            raise ValueError(
                f"Invalid configuration: Start point {self.start} is blocked. "
                "Start point cannot be part of the blocked pattern."
            )
        if self.end in self.blocked:
            raise ValueError(
                f"Invalid configuration: End point {self.end} is blocked. "
                "End point cannot be part of the blocked pattern."
            )

    def _remove_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Removes the wall between two adjacent cells.
        Blocked cells are protected and never modified.
        """
        if (x1, y1) in self.blocked or (x2, y2) in self.blocked:
            return

        if x2 == x1 and y2 == y1 - 1:
            direction = Direction.NORTH
        elif x2 == x1 + 1 and y2 == y1:
            direction = Direction.EAST
        elif x2 == x1 and y2 == y1 + 1:
            direction = Direction.SOUTH
        elif x2 == x1 - 1 and y2 == y1:
            direction = Direction.WEST
        else:
            return

        self.grid[y1][x1] &= ~direction
        self.grid[y2][x2] &= ~Direction.opposite(direction)

    def make_imperfect(self, threshold: float = 0.005) -> None:
        """
        Removes random internal walls to create loops (cycles) in the maze.
        This turns a Perfect Maze into an Imperfect Maze.

        Args:
            threshold: Probability of removing a wall per cell
            (small value recommended).
        """
        directions = [
            Direction.NORTH, Direction.SOUTH,
            Direction.EAST, Direction.WEST
        ]

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.blocked:
                    continue
                if (x, y) in {self.start, self.end}:
                    continue
                if random.random() >= threshold:
                    continue

                candidates: List[Tuple[int, int]] = []

                for d in directions:
                    if self.grid[y][x] & d:
                        nx, ny = x, y
                        if d == Direction.NORTH:
                            ny -= 1
                        elif d == Direction.SOUTH:
                            ny += 1
                        elif d == Direction.EAST:
                            nx += 1
                        elif d == Direction.WEST:
                            nx -= 1

                        if (
                            0 <= nx < self.width
                            and 0 <= ny < self.height
                            and (nx, ny) not in self.blocked
                        ):
                            candidates.append((nx, ny))

                if candidates:
                    nx, ny = random.choice(candidates)
                    self._remove_wall(x, y, nx, ny)

    def solve(self, renderer: Optional[MazeRenderer] = None,
              delay: float = 0.5, show_path: bool = True) -> str:
        """
        Solves the maze using BFS to find the shortest valid path.
        """
        queue = deque([(self.start[0], self.start[1], "")])
        visited = {self.start}

        moves = [
            (Direction.NORTH, 0, -1, 'N'),
            (Direction.SOUTH, 0, 1, 'S'),
            (Direction.EAST, 1, 0, 'E'),
            (Direction.WEST, -1, 0, 'W')
        ]

        while queue:
            cx, cy, path = queue.popleft()
            current = (cx, cy)

            if current == self.end:
                self.solution_path = path
                self.solution_cells = self._path_to_cells(path)

                # Animate the solution path when found
                if renderer and show_path:
                    renderer.render_path_animated(
                        walked_path=self.solution_cells,
                        delay=delay,
                        visited=visited
                    )
                return path

            for direction, dx, dy, char in moves:
                nx, ny = cx + dx, cy + dy

                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if (nx, ny) in self.blocked:
                    continue
                if self.grid[cy][cx] & direction:
                    continue
                if (nx, ny) in visited:
                    continue

                visited.add((nx, ny))
                queue.append((nx, ny, path + char))

        self.solution_path = None
        self.solution_cells = None
        return ""

    def _path_to_cells(self, path: str) -> List[Tuple[int, int]]:
        """
        Converts BFS path string like 'NSEW' into ordered list of coordinates.
        """
        x, y = self.start
        cells = [(x, y)]
        for move in path:
            if move == 'N':
                y -= 1
            elif move == 'S':
                y += 1
            elif move == 'E':
                x += 1
            elif move == 'W':
                x -= 1
            cells.append((x, y))
        return cells

    @abstractmethod
    def generate(self, delay: float = 0.02,
                 renderer: Optional[MazeRenderer] = None) -> None:
        """
        Child classes must implement the maze generation logic.
        """
        pass
