# mazegen - Maze Generation Library

Reusable Python library for maze generation and solving.

This module contains only maze logic and is fully independent from rendering,
user input, or application-specific code.

---

## Public API

```python
from mazegen import MazeFactory, MazeGenerator
```

- MazeGenerator — abstract base class implementing shared maze logic
- MazeFactory — factory used to instantiate concrete maze generators

---

## MazeGenerator

MazeGenerator is an abstract base class implementing common behavior:

- grid initialization using bitwise wall representation
- entry and exit handling
- mandatory embedded “42” pattern
- consistent wall removal between adjacent cells
- shortest-path solving using Breadth-First Search (BFS)
- optional conversion from perfect to imperfect mazes

Concrete generators must implement the generate() method.

---

## Supported Algorithms

Generators are selected by name using the factory.

Available algorithms:

- backtracker — Recursive Backtracker (Depth-First Search)
- wilson — Wilson’s algorithm (uniform spanning tree)

---

## Basic Usage

```python
from mazegen import MazeFactory

generator = MazeFactory.get_maze_generator(
    algorithm="backtracker",
    width=20,
    height=15,
    seed=42
)

generator.generate()
generator.make_imperfect(threshold=0.005)
path = generator.solve()

print(path)
```

---

## Maze Representation

Each cell is stored as a single integer using a 4-bit encoding:

- bit 0 — North
- bit 1 — East
- bit 2 — South
- bit 3 — West

A set bit means the wall is closed.
This representation is compatible with hexadecimal maze output formats.

---

## Special Constraints

- A visible “42” pattern is embedded using permanently blocked cells
- Blocked cells are never modified during generation or solving
- Wall coherence and full connectivity rules are always enforced

If the maze is too small to draw the “42” pattern, generation continues
without it and an error message is printed.

---

## Path Solving

Maze solving is implemented using Breadth-First Search (BFS), guaranteeing
the shortest valid path between the entry and exit points.

The solution is returned as:
- a string of directions (N, E, S, W)
- an ordered list of visited cells

---

## Design

The library follows the Template Method pattern:

- shared logic is implemented in MazeGenerator
- algorithm-specific behavior is implemented in child classes

Algorithm selection is handled via a Factory pattern, allowing new
generators to be added without modifying existing code.

---

## Scope

mazegen contains no rendering, input handling, or UI logic.
It is intended to be reused in other projects.
