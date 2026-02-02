"""Utility functions for the maze application."""
import os


def clear() -> None:
    """Clear the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")
