import sys
import os
from typing import Optional

from mazegen import get_maze_generator, MazeGenerator


def parse_config(file_path: str) -> dict[str, str]:
    """
    Parse a key=value configuration file.
    Keys are case-insensitive.
    Lines starting with '#' or empty lines are ignored.
    """
    config: dict[str, str] = {}

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            config[key.strip().upper()] = value.strip()

    return config


def parse_point(value: str) -> tuple[int, int]:
    """
    Parse a coordinate in the form 'x,y'.
    """
    try:
        x_str, y_str = value.split(",")
        return int(x_str), int(y_str)
    except Exception:
        raise ValueError(f"Invalid coordinate format: '{value}'")


def save_maze_to_file(
    generator: MazeGenerator,
    filename: str,
    solution: str
) -> None:
    """
    Save the maze grid, start/end coordinates and solution path
    to a file in the required output format.
    """
    with open(filename, "w") as f:
        for row in generator.grid:
            f.write("".join(f"{cell:X}" for cell in row) + "\n")

        f.write("\n")
        f.write(f"{generator.start[0]},{generator.start[1]}\n")
        f.write(f"{generator.end[0]},{generator.end[1]}\n")
        f.write(solution + "\n")


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

    try:
        generator = get_maze_generator(
            algorithm=algorithm,
            width=width,
            height=height,
            seed=seed,
        )
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Apply entry / exit from config
    generator.start = entry
    generator.end = exit_

    # Generation pipeline
    generator.generate()

    if not perfect:
        print("Creating imperfect maze (adding cycles)...")
        generator.make_imperfect()

    print("Solving maze...")
    solution = generator.solve()

    try:
        save_maze_to_file(generator, output_file, solution)
        print(f"Maze successfully saved to '{output_file}'")
    except OSError as e:
        print(f"Error writing output file: {e}")


if __name__ == "__main__":
    main()
