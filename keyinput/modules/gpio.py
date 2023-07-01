from ..base_module import ButtonModule

from gpiozero import Button


class GPIOButtons(ButtonModule):

    def __init__(self):
        self.buttons = [
            Button(17),
            Button(4)
        ]

    def check_status(self, buttonID: int) -> bool:
        return self.buttons[buttonID].is_active
