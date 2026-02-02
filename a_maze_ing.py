import sys
import os
from typing import Optional
from mazegen import MazeFactory
from renderer import ASCIIMazeRenderer
from utils import clear, save_maze_to_file, parse_config, parse_point
import readchar


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    config_path = sys.argv[1]

    if not os.path.isfile(config_path):
        print(f"Error: Config file '{config_path}' not found.")
        return

    try:
        config = parse_config(config_path)
    except OSError as e:
        print(f"Error reading config file: {e}")
        return

    try:
        width: int = int(config.get("WIDTH", 20))
        height: int = int(config.get("HEIGHT", 20))
        algorithm: str = config.get("ALGO", "backtracker")
        output_file: str = config.get("OUTPUT_FILE", "maze.txt")

        seed: Optional[int] = (
            int(config["SEED"]) if "SEED" in config else None
        )
        perfect: bool = config.get("PERFECT", "true").lower() == "true"

        entry: tuple[int, int] = (
            parse_point(config["ENTRY"])
            if "ENTRY" in config
            else (0, 0)
        )

        exit_: tuple[int, int] = (
            parse_point(config["EXIT"])
            if "EXIT" in config
            else (width - 1, height - 1)
        )

    except ValueError as e:
        print(f"Configuration error: {e}")
        return

    print(f"Initializing {algorithm.upper()} generator ({width}x{height})")

    wall_color: str = "magenta"
    blocked_color: str = "red"
    path_color: str = "yellow"
    visited_color: str = "cyan"
    frontier_color: str = "blue"
    current_color: str = "red"
    background_color: Optional[str] = None

    path_visible = True
    regen = True
    delay = 0.05
    maze = MazeFactory.get_maze_generator(
        algorithm=algorithm,
        width=width,
        height=height,
        seed=seed
    )
    maze.start = entry
    maze.end = exit_
    while True:
        clear()
        if regen:
            maze = MazeFactory.get_maze_generator(
                algorithm=algorithm,
                width=width,
                height=height,
                seed=seed
            )
            maze.start = entry
            maze.end = exit_

        # Convert background color to termcolor format (on_<color>)
        bg = f"on_{background_color}" if background_color else None

        renderer = ASCIIMazeRenderer(
            maze,
            wall_color=wall_color,
            start_color="green",
            end_color="red",
            path_color=path_color,
            visited_color=visited_color,
            frontier_color=frontier_color,
            current_color=current_color,
            blocked_color=blocked_color,
            background=bg
        )
        if regen:
            maze.generate(delay=delay, renderer=renderer)
            if not perfect:
                maze.make_imperfect()
            regen = False

        # Show the maze first
        renderer.render()

        # Solve and animate path only if path_visible is True
        path = maze.solve(renderer=renderer if path_visible else None,
                          delay=delay,
                          show_path=path_visible)
        if maze.message_42:
            print("\n" + maze.message_42)
        print(
            str("\nCommands: [SPACE] regenerate |"
                " [P] toggle path | [C] change colors | [Q] quit"))
        key = readchar.readchar().lower()

        if key == "q":
            break
        elif key == " ":
            regen = True  # regenerate
        elif key == "p":
            path_visible = not path_visible
        elif key == "c":
            # Change colors
            print(str("\nAvailable colors: red, green, yellow,"
                  " blue, magenta, cyan, white"))
            print("(Leave empty to keep current color)\n")

            c = input("Wall color: ")
            if c:
                c = c.strip().lower()
                wall_color = c

            c = input("42 pattern color: ")
            if c:
                c = c.strip().lower()
                blocked_color = c

            c = input(
                "Background color: ")
            if c:
                c = c.strip().lower()
                background_color = None if c == "none" else c

    # Save maze on exit
    try:
        save_maze_to_file(maze, output_file, "".join(path))
        print(f"Maze saved to '{output_file}'")
    except Exception as e:
        print(f"Error saving maze: {e}")


if __name__ == "__main__":
    main()
