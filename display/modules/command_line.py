"""
A command line display emulator
"""
from static_info import VERSION
from ..base_module import DisplayModule, DisplaySize
from sys import stdout

SIZE = (20, 4)


class CommandLineDisplay(DisplayModule):
    """
    A command line display emulator
    """

    def __init__(self):
        """
        Initialize the command line display module
        """
        super().__init__(DisplaySize(*SIZE))
        print(f"orc {VERSION} testing CLI display")
        print("-----------------------------------")
        for i in range(4):
            print("")  # Print one clear line at the start and then the four empty lines of the display
        #print(f"size: {self.size.x}x{self.size.y} - :)", end="")
        print("\033[F")
        stdout.flush()

    def display_line(self, line: int, content: str):
        """
        Update a line in the command lines
        :param line: Line to update
        :param content: Content to display
        :return:
        """
        if line < 0 or line > 3:
            raise ValueError("Line must be between 0 and 3 (4 lines)")
        print(("\033[A" * (4 - line)) + "\x1b[2K" + content + ("\033[B" * (4 - line - 1)))
