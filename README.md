*This project has been created as part of the 42 curriculum by jmanani, mlagutin.*

# A-Maze-Ing

An advanced maze generation and visualization tool written in Python, featuring multiple generation algorithms, an interactive terminal-based UI with customizable colors, animated pathfinding, and a reusable maze generation module.

---

## Quick Start

```bash
# Install dependencies
make install

# Run with default configuration
make run config.txt

# Run with custom configuration
make run your_config.txt

# Clean build artifacts
make clean
```

---

## Description

**A-Maze-Ing** is a maze generation project designed to explore algorithmic maze construction, graph traversal, and clean software architecture.

The program reads a configuration file, generates a valid maze respecting strict structural constraints, visually renders the maze in the terminal, and computes the shortest path between an entry and an exit point. All generation logic is encapsulated in a reusable module, allowing the maze generator to be reused independently of the visualization layer.

---

## Configuration

The application reads a `config.txt` file with the following parameters:

| Parameter | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| `WIDTH` | int | 20 | Maze width (must be positive) |
| `HEIGHT` | int | 20 | Maze height (must be positive) |
| `ENTRY` | x,y | 0,0 | Entry point coordinates (0-indexed) |
| `EXIT` | x,y | WIDTH-1,HEIGHT-1 | Exit point coordinates |
| `ALGO` | string | backtracker | Generation algorithm: `backtracker` or `wilson` |
| `PERFECT` | bool | true | Generate perfect maze (no loops) or imperfect |
| `OUTPUT_FILE` | string | maze.txt | Output filename for maze data |
| `SEED` | int | (none) | Random seed for reproducibility (optional) |


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

During execution, use the following keyboard controls in real time:

| Key | Action |
| --- | ------ |
| **SPACE** | Regenerate the maze with the same algorithm |
| **P** | Toggle shortest-path visualization on/off |
| **C** | Change colors |
| **Q** | Quit the application |

## Usage

### Running the Application

```bash
# Run with default config
python3 a_maze_ing.py config.txt

# Or using make
make run config.txt

# Debug mode with Python debugger
make debug config.txt
```

### Output Format

The maze is saved to the configured output file (default: `maze.txt`) in the following format:

```
[Grid as hexadecimal - one digit per cell]

[Entry coordinates: x,y]
[Exit coordinates: x,y]
[Solution path: sequence of N/E/S/W directions]
```

Each cell's hexadecimal digit represents walls in all four directions (bit encoding: N=1, E=2, S=4, W=8).

---

## Development & Maintenance

### Code Quality

```bash
# Run linting and type checks
make lint

# Strict mode (more rigorous checks)
make lint-strict

# Clean build artifacts
make clean
```

### Project Structure

```
.
├── a_maze_ing.py              # Main application entry point
├── config.txt                 # Configuration file
├── utils.py                   # Utility functions
├── mazegen/                   # Reusable maze generation module
│   ├── generator.py           # Base MazeGenerator class
│   ├── factory.py             # MazeFactory for algorithm selection
│   ├── backtracker.py         # Recursive Backtracker (DFS)
│   ├── wilson.py              # Wilson's Algorithm
│   └── __init__.py            # Module exports
├── renderer/                  # Terminal rendering module
│   ├── render.py              # ASCIIMazeRenderer
│   └── __init__.py            # Module exports
└── README.md                  # This file
```

---

## Reusable Maze Generator Module

The `mazegen` module is fully reusable and independent from rendering or user input.

### Module Features

- **Common `MazeGenerator` interface** — all algorithms share a unified base
- **MazeFactory pattern** — dynamic algorithm selection
- **Generation, imperfection, and solving logic** — complete maze lifecycle
- **Standalone packaging** — can be installed independently

### Using the Module

```python
from mazegen import MazeFactory

# Create a maze generator
generator = MazeFactory.get_maze_generator(
    algorithm="backtracker",
    width=20,
    height=20,
    seed=42
)

# Set entry and exit points
generator.start = (0, 0)
generator.end = (19, 19)

# Generate the maze
generator.generate()

# Solve it
solution_path = generator.solve()  # Returns "EESSWWNNN..."

# Access the grid
grid = generator.grid  # 2D list of hex-encoded cell values
```

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

## Team & Contributions

**Mariia Lagutina (mlagutin)**
Maze generation algorithms, reusable `mazegen` module, core architecture, BFS pathfinding, 42 pattern logic, Makefile and project setup

**Jayesh Manani (jmanani)**
Terminal renderer, ASCII visualization, animations, color design, user interaction, refractoring code

---

## Project Development

### Approach

The project was developed iteratively, starting with core maze validity and constraints, followed by algorithm implementation, visualization, and finally packaging and documentation.

### Key Achievements

- Clear separation between generation and rendering layers
- Reusable and extensible architecture enabling independent module usage
- Interactive visualization providing real-time debugging and validation

### Future Enhancements

- Additional generation algorithms (Kruskal, Prim)
- Alternative rendering backends (graphical UI, web-based)
- Comprehensive automated test suite

---

## AI Integration

To ensure high code quality, LLM-based tools were used for:

- Analyzing complex design patterns for edge-case coverage
- Validating deployment and packaging scripts
- Proofreading technical documentation

The team maintained full control over the codebase, reviewing and adapting all suggestions to meet specific project constraints.
