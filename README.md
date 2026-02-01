*This project has been created as part of the 42 curriculum by jmanani, mlagutin.*

# A-Maze-Ing

An advanced maze generation and visualization tool written in Python, featuring multiple generation algorithms, an interactive terminal-based UI with customizable colors, animated pathfinding, and a reusable maze generation module.

---

## Description

**A-Maze-Ing** is a maze generation project designed to explore algorithmic maze construction, graph traversal, and clean software architecture.

The program reads a configuration file, generates a valid maze respecting strict structural constraints, visually renders the maze in the terminal, and computes the shortest path between an entry and an exit point. All generation logic is encapsulated in a reusable module, allowing the maze generator to be reused independently of the visualization layer.

---

## Project Goals

* Generate valid mazes that respect all subject constraints
* Support both perfect and imperfect maze generation
* Provide interactive, real-time terminal visualization
* Compute and visualize shortest paths automatically
* Ensure reproducible results via optional seeding
* Output a verifiable maze representation to a file
* Offer a reusable and extensible maze generation module

---

## Architecture Overview

The project is organized around a clear separation of responsibilities:

* **mazegen/** — reusable maze generation module
* **renderer/** — ASCII-based terminal visualization
* **a_maze_ing.py** — application entry point and interaction loop

Maze generation, rendering, and user interaction are fully decoupled, improving clarity, testability, and extensibility.

---

## Maze Generation Design

### Base Generator (`MazeGenerator`)

All maze generators inherit from an abstract base class implementing shared behavior:

* grid initialization using a bitwise wall representation
* entry and exit management
* mandatory “42” pattern placement
* pathfinding using Breadth-First Search (BFS)
* optional conversion from perfect to imperfect mazes

The base class uses the **Template Method pattern**, ensuring correctness while allowing algorithms to specialize only the generation step.

### Wall Representation

Each cell is stored as a single integer using a 4-bit encoding:

| Bit | Direction |
| --- | --------- |
| 0   | North     |
| 1   | East      |
| 2   | South     |
| 3   | West      |

Walls are removed using bitwise operations. This compact representation directly matches the hexadecimal output format required by the subject.

---

## Maze Factory

Maze generation algorithms are selected dynamically using a factory pattern.

The `MazeFactory` maps algorithm names provided in the configuration file to concrete generator classes. This allows new algorithms to be added without modifying the main application logic.

Supported algorithms:

* **backtracker** — Recursive Backtracker (Depth-First Search)
* **wilson** — Wilson’s algorithm (loop-erased random walks)

---

## Maze Generation Algorithms

### Recursive Backtracker (Depth-First Search)

The recursive backtracker algorithm explores the maze using an iterative depth-first search:

1. Start from the entry cell
2. Randomly choose an unvisited neighboring cell
3. Remove the wall between the current cell and the neighbor
4. Continue until no unvisited neighbors remain, then backtrack

This algorithm generates perfect mazes with long corridors and guarantees a unique path between any two cells.

Blocked cells forming the “42” pattern are treated as permanently visited and are never modified.

---

### Wilson’s Algorithm

Wilson’s algorithm generates mazes using loop-erased random walks, producing **uniformly distributed spanning trees**.

The algorithm:

* selects a random starting cell
* performs a random walk until it reaches an already visited cell
* erases loops encountered during the walk
* carves the final loop-erased path into the maze

Although slower than DFS, Wilson’s algorithm reduces directional bias and provides a high-quality alternative generation method.

---

## Pathfinding

Maze solving is implemented using **Breadth-First Search (BFS)**, guaranteeing the shortest valid path between the entry and exit points.

The solver:

* respects all wall constraints
* avoids blocked cells (including the “42” pattern)
* returns the solution as a sequence of directions (`N`, `E`, `S`, `W`)
* optionally animates the solving process in the terminal

The solution is also converted into a list of visited cells for visualization and output generation.

---

## Interactive Terminal Renderer

Maze visualization is handled by the `ASCIIMazeRenderer`, which renders the maze using ASCII characters and terminal colors.

Features include:

* colored walls, paths, and markers using `termcolor`
* animated maze generation and solving
* directional arrows indicating path traversal
* optional background coloring

### Interactive Controls

During execution, the following keyboard controls are available:

* **SPACE** — regenerate the maze
* **P** — toggle shortest-path visualization
* **C** — change colors (walls, pattern, background)
* **Q** — quit the application

All interactions are handled in real time using single-key input.

---

## Output File Format

The generated maze is written to an output file using one hexadecimal digit per cell, encoding the wall configuration.

After the grid representation, the file contains:

1. an empty line
2. entry coordinates
3. exit coordinates
4. the shortest path expressed as `N`, `E`, `S`, `W`

This output format can be validated automatically using the script provided with the subject.

---

## Reusable Maze Generator Module

The `mazegen` module is fully reusable and independent from rendering or user input.

It exposes:

* a common `MazeGenerator` interface
* a factory for algorithm selection
* generation, imperfection, and solving logic

The module can be packaged and installed independently using standard Python packaging tools.

---

## Resources

### Maze Generation Algorithms

* Wikipedia — Maze Generation Algorithms
  [https://en.wikipedia.org/wiki/Maze_generation_algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

* Recursive Backtracker Explained
  [https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)

* Wilson’s Algorithm (UST)
  [https://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm](https://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm)

### Graph Traversal & Pathfinding

* Breadth-First Search (BFS) — GeeksforGeeks
  [https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)

* BFS Pathfinding in Grids
  [https://www.redblobgames.com/pathfinding/a-star/introduction.html](https://www.redblobgames.com/pathfinding/a-star/introduction.html)

### Python & Design Patterns

* Python `abc` module (Abstract Base Classes)
  [https://docs.python.org/3/library/abc.html](https://docs.python.org/3/library/abc.html)

* Factory Pattern — Refactoring Guru
  [https://refactoring.guru/design-patterns/factory-method](https://refactoring.guru/design-patterns/factory-method)

* Template Method Pattern
  [https://refactoring.guru/design-patterns/template-method](https://refactoring.guru/design-patterns/template-method)

---

## Team & Project Management

### Team Members

- **Mariia Lagutina (mlagutin)** — maze generation algorithms, reusable `mazegen` module, core architecture, BFS pathfinding, 42 pattern logic, Makefile and project setup
- **Jayesh Manani (jmanani)** — terminal renderer, ASCII visualization, animations, color design, user interaction


### Planning & Evolution

The project was developed iteratively, starting with core maze validity and constraints, followed by algorithm implementation, visualization, and finally packaging and documentation.

### What Worked Well

* clear separation between generation and rendering
* reusable and extensible architecture
* interactive visualization aiding debugging and validation

### What Could Be Improved

* additional generation algorithms (Kruskal, Prim)
* alternative rendering backends (graphical UI)
* more extensive automated testing

---

## Use of AI

Artificial Intelligence Integration Policy

To ensure high code quality, LLM-based tools were used for static analysis and refinement to:

* analyze complex design patterns for edge-case coverage

* validate deployment and packaging scripts

* proofread technical documentation for professional terminology

The team maintained full control over the codebase, reviewing and adapting all suggestions to meet specific project constraints.
