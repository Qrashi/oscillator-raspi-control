from ..base_module import TemperatureProvider


class StaticTempSimulator(TemperatureProvider):
    """
    Static temperature simulator - since temperature is really not that important
    """
    def get(self):
        return 10.0
