import select
import sys
import termios
import tty

from ..base_module import ButtonModule

class CLIButtons(ButtonModule):

    keymap = {
        'e': 0,
        '\r': 1
    }

    def __init__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    def check_status(self, buttonID: int) -> bool:
        key = sys.stdin.read(1)
        if key in self.keymap:
            return self.keymap[key] == buttonID
        return False

    def end(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)