import abc


class TemperatureProvider(abc.ABC):

    @abc.abstractmethod
    def get(self) -> float:
        """
        Get the current temperature
        :return:
        """
