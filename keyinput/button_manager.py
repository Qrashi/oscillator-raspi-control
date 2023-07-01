from .base_module import ButtonModule

class ButtonManager:

    def __init__(self, button_module: ButtonModule):
        self.button_module = button_module

    def experiment(self) -> bool:
        """
        Get the status of the experiment button
        :return:
        """
        return self.button_module.check_status(0)

    def confirmed(self) -> bool:
        """
        Return the status of the conform button
        :return:
        """
        return self.button_module.check_status(1)
