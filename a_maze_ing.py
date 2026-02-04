import sys
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

    try:
        config = parse_config(config_path)
    except Exception as e:
        print(f"Parsing Error: {e}")
        return

    try:
        width: int = int(config.get("WIDTH", 20))
        height: int = int(config.get("HEIGHT", 20))
        algorithm: str = config.get("ALGO", "backtracker")
        op_file_path: str = str(config.get("OUTPUT_FILE", "")).strip().strip(
            "\"").strip("'").strip()
        output_file: str = op_file_path or "maze.txt"

        seed: Optional[int] = (
            int(config["SEED"]) if "SEED" in config else None
        )
        perfect: bool = config.get("PERFECT", "true").lower() == "true"

        entry: tuple[int, int] = (
            parse_point(config["ENTRY"])
            if "ENTRY" in config
            else (0, 0)
        )
        if (entry[0] < 0 or entry[1] < 0 or
                entry[0] >= width or entry[1] >= height):
            raise ValueError("ENTRY point is out of maze bounds.")

        exit_: tuple[int, int] = (
            parse_point(config["EXIT"])
            if "EXIT" in config
            else (width - 1, height - 1)
        )
        if (exit_[0] < 0 or exit_[1] < 0 or
                exit_[0] >= width or exit_[1] >= height):
            raise ValueError("EXIT point is out of maze bounds.")

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
    try:
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
                if renderer:
                    maze.generate(delay=delay, renderer=renderer)
                else:
                    maze.generate()
                if not perfect:
                    maze.make_imperfect()
                regen = False

            # Show the maze first
            renderer.render()

            # Solve and animate path only if path_visible is True
            path = maze.solve(renderer=renderer,
                              delay=delay,
                              show_path=path_visible)
            save_maze_to_file(maze, output_file, "".join(path))
            print(f"Maze saved to '{output_file}'")
            if maze.message_42:
                print("\n" + maze.message_42)
            print(
                str("\nCommands: [SPACE] regenerate |"
                    " [P] toggle path | [C] change colors | [Q] quit"))
            key = readchar.readchar()
            if key == "\x03":
                raise KeyboardInterrupt
            key = key.lower()

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

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()
