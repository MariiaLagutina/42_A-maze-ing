import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Set
from collections import deque

# Constants for bitwise wall representation
NORTH = 0b0001  # 1
EAST = 0b0010   # 2
SOUTH = 0b0100  # 4
WEST = 0b1000   # 8
ALL_WALLS = 0b1111  # 15 (0xF)

# Helper for removing walls in the opposite direction
OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}

# Minimal size required to draw the "42" pattern safely
MIN_WIDTH_FOR_42 = 12
MIN_HEIGHT_FOR_42 = 10


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

        if seed is not None:
            random.seed(seed)

        # Initialize grid: all cells start with all walls closed
        self.grid: List[List[int]] = [
            [ALL_WALLS for _ in range(width)] for _ in range(height)
        ]

        self.start: Tuple[int, int] = (0, 0)
        self.end: Tuple[int, int] = (width - 1, height - 1)

        # Permanently blocked cells (the "42" pattern)
        self.blocked: Set[Tuple[int, int]] = set()

    def _draw_42(self) -> None:
        """
        Draws the '42' pattern centered in the grid by adding coordinates
        to the blocked set. Blocked cells remain fully closed.
        """
        if self.width < MIN_WIDTH_FOR_42 or self.height < MIN_HEIGHT_FOR_42:
            print("Error: Maze too small for '42' pattern.")
            return

        cx, cy = self.width // 2, self.height // 2

        digit_4 = [
            (-4, -2), (-2, -2),
            (-4, -1), (-2, -1),
            (-4, 0), (-3, 0), (-2, 0),
            (-2, 1),
            (-2, 2)
        ]

        digit_2 = [
            (1, -2), (2, -2), (3, -2),
            (3, -1),
            (1, 0), (2, 0), (3, 0),
            (1, 1),
            (1, 2), (2, 2), (3, 2)
        ]

        for dx, dy in digit_4 + digit_2:
            x, y = cx + dx, cy + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.blocked.add((x, y))

    def _remove_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Removes the wall between two adjacent cells.
        Blocked cells are protected and never modified.
        """
        if (x1, y1) in self.blocked or (x2, y2) in self.blocked:
            return

        if x2 == x1 and y2 == y1 - 1:
            direction = NORTH
        elif x2 == x1 + 1 and y2 == y1:
            direction = EAST
        elif x2 == x1 and y2 == y1 + 1:
            direction = SOUTH
        elif x2 == x1 - 1 and y2 == y1:
            direction = WEST
        else:
            return

        self.grid[y1][x1] &= ~direction
        self.grid[y2][x2] &= ~OPPOSITE[direction]

    def make_imperfect(self, threshold: float = 0.05) -> None:
        """
        Removes random internal walls to create loops (cycles) in the maze.
        This turns a Perfect Maze into an Imperfect Maze.

        Args:
            threshold: Probability of removing a wall per cell
            (small value recommended).
        """
        directions = [NORTH, SOUTH, EAST, WEST]

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
                        if d == NORTH:
                            ny -= 1
                        elif d == SOUTH:
                            ny += 1
                        elif d == EAST:
                            nx += 1
                        elif d == WEST:
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

    def solve(self) -> str:
        """
        Solves the maze using BFS to find the shortest valid path.
        """
        queue = deque([(self.start[0], self.start[1], "")])
        visited = {self.start}

        moves = [
            (NORTH, 0, -1, 'N'),
            (SOUTH, 0, 1, 'S'),
            (EAST, 1, 0, 'E'),
            (WEST, -1, 0, 'W')
        ]

        while queue:
            cx, cy, path = queue.popleft()

            if (cx, cy) == self.end:
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

        return ""

    @abstractmethod
    def generate(self) -> None:
        """
        Child classes must implement the maze generation logic.
        """
        pass
