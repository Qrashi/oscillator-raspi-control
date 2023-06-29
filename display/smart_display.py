"""
File containing the SmartDisplay API
"""

from display.base_module import DisplayModule, DisplayContent
from typing import Dict, List, Union


class SmartDisplay:
    """
    A display API to make using a DisplayModule easier

    This API can experience rapid changes
    """
    _display: DisplayModule

    def __init__(self, display: DisplayModule):
        """
        Initialize a new display API
        :param display:
        """
        self._display = display
        # I have to learn asyncio

    def get_content(self) -> DisplayContent:
        """
        Get a description of the current display
        :return:
        """
        return self._display.get_content()

    def clear(self, line: int = -1):
        """
        Clear a line (-1 for all)
        :param line:
        :return:
        """
        if line == -1:
            self._display.display(0, "")
            self._display.display(1, "")
            self._display.display(2, "")
            self._display.display(3, "")
            return
        self._display.display(line, "")

    def right(self, line: int, content: str):
        """
        Display content at the ride side of the display
        :param line: Line to display at
        :param content: Content to display
        :return:
        """
        if len(content) > self._display.size.x:
            raise ValueError("Content is too long to fit line")
        # Figure out how much to pad
        pad = self._display.size.x - len(content)
        # display the padded content
        self._display.display(line, " " * pad + content)

    def left(self, line: int, content: str):
        """
        Display content at the left side of the display
        :param line: Line to display at
        :param content: Content to display
        :return:
        """
        if len(content) > self._display.size.x:
            raise ValueError("Content is too long to fit line")
        # display the padded content
        self._display.display(line, content)

    def center(self, line: int, content: str):
        """
        Display a text centered in a specific line
        :param line: Line to display at
        :param content: Content to display
        :return:
        """
        if len(content) > self._display.size.x:
            raise ValueError("Content is too to fit line")
        # Figure out how much to pad
        pad = (self._display.size.x - len(content)) // 2
        # display the padded content
        self._display.display(line, " " * pad + content + " " * pad)

    def left_right(self, line: int, left: str, right: str):
        """
        Display content on the left and right side of the display
        :param line: The line to display at
        :param left: Content of left side of display
        :param right: Content of right side of display
        :return:
        """
        if len(left) + len(right) > self._display.size.x:
            raise ValueError("Content is too long to fit line")
        # display the padded content
        self._display.display(line, left + " " * (self._display.size.x - len(left) - len(right)) + right)

    def menu(self, content: str):
        """
        Display the current UI location of the user and fill the rest with the line with -
        :param content: Current UI location
        :return:
        """
        self._display.display(0, "-> " + content + "-" * (self._display.size.x - len(content) + 3))
