"""Contains only the main method. This is where it all begins."""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from src.control_unit import ControlUnit


def main():
    """Calls the control unit to start the game instance"""
    cu = ControlUnit()
    cu.game_loop()


if __name__ == "__main__":
    # execute only if run as a script. Prevents accidental imports from starting another game.
    main()
