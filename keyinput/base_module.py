import abc


class ButtonModule(abc.ABC):
    """
    Defines buttons, this code is very much insanely bad but please ignore, it just needs to work
    """

    @abc.abstractmethod
    def check_status(self, buttonID: int) -> bool:
        """
        Return status of a button
        :param buttonID: button to return status of
        :return:
        """

    def end(self):
        """
        Terminate key-checking
        :return:
        """

