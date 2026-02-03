"""Utility functions for the maze application."""
import os
from mazegen import MazeGenerator


def clear() -> None:
    """Clear the terminal screen."""
    try:
        os.system("clear" if os.name == "posix" else "cls")
    except Exception:
        raise RuntimeError("Unable to clear the terminal screen.")


def save_maze_to_file(
    generator: MazeGenerator,
    filename: str,
    solution: str
) -> None:
    """
    Save the maze grid, start/end coordinates and solution path
    to a file in the required output format.
    """
    try:
        with open(filename, "w") as f:
            for row in generator.grid:
                f.write("".join(f"{cell:X}" for cell in row) + "\n")

            f.write("\n")
            f.write(f"{generator.start[0]},{generator.start[1]}\n")
            f.write(f"{generator.end[0]},{generator.end[1]}\n")
            f.write(solution + "\n")
    except Exception as e:
        raise ValueError(f"Error While Saving Maze - {type(e).__name__} - {e}")


def parse_point(value: str) -> tuple[int, int]:
    """
    Parse a coordinate in the form 'x,y'.
    """
    try:
        x_str, y_str = value.split(",")
        return int(x_str), int(y_str)
    except Exception as e:
        raise ValueError(f"Invalid coordinate format: '{value}' - {e}")


def parse_config(file_path: str) -> dict[str, str]:
    """
    Parse a key=value configuration file.
    Keys are case-insensitive.
    Lines starting with '#' or empty lines are ignored.
    """
    config: dict[str, str] = {}
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"Config file '{file_path}' not found.")

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
    except Exception as e:
        raise ValueError(f"{e}")
