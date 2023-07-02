import singlejson
from singlejson import load

from .base_module import TemperatureProvider


def init() -> TemperatureProvider:
    if load("device.json", default={"device_type": "pc"}).json["device_type"] == "pi":
        from .modules.raspi_temps import RaspiTemp
        return RaspiTemp()
    from .modules.static_temp import StaticTempSimulator
    return StaticTempSimulator()
