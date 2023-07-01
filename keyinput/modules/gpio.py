from ..base_module import ButtonModule

from gpiozero import Button


class GPIOButtons(ButtonModule):

    def __init__(self):
        self.buttons = [
            Button(4),
            Button(17)
        ]

    def check_status(self, buttonID: int) -> bool:
        return self.buttons[buttonID].is_held
