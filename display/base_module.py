from __future__ import annotations

"""
The template for a module
"""

"""
Current display format:
| current location
| action list
| action list
time, internet status
--> we can set line content
"""
import abc

from typing import List


class DisplaySize:
    """
    Defines a size of a display
    """
    x: int
    y: int

    def __init__(self, x: int, y: int):
        """
        Create a new DisplaySize
        :param x: x size
        :param y: y size
        """
        self.x = x
        self.y = y


class DisplayContent:
    """
    A class defining what is currently being displayed on the display
    """
    _content: List[str]
    _display: DisplayModule

    def __init__(self, content: List[str], display: DisplayModule):
        """
        Initialize a new DisplayContent class holding the current state of the display
        :param content:
        """
        self._content = content
        self._display = display

    def apply(self):
        """
        Apply the content back to the display
        :return:
        """
        for line, content in enumerate(self._content):
            self._display.display(line, content)


class DisplayModule(abc.ABC):
    """
    Defines a display

    contains all important bare metal functions
    """
    size: DisplaySize
    _content: List[str] = ["", "", "", ""]

    def __init__(self, size: DisplaySize):
        """
        Initialize the display
        :param size: Size of the display
        :return:
        """
        self.size = size

    def get_content(self) -> DisplayContent:
        """
        Get a description of the current screen contents
        :return:
        """
        return DisplayContent(self._content, self)

    @abc.abstractmethod
    def display_line(self, line: int, content: str):
        """
        The function that needs to be implemented; display content on a line
        :param line:
        :param content:
        :return:
        """

    def display(self, line: int, content: str):
        """
        Display text at a specific line (avialible to use for everyone)
        :param line: The line to display at
        :param content: Content to display
        :return:
        """
        content = content.replace("\n", "")
        self._content[line] = content
        self.display_line(line, content)
