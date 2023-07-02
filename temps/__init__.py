import singlejson
from singlejson import load

from .tempkeeper import TempKeeper


def init() -> TempKeeper:
    if load("device.json", default={"device_type": "pc"}).json["device_type"] == "pi":
        from .modules.raspi_temps import RaspiTemp
        return TempKeeper(RaspiTemp(), 3)
    from .modules.static_temp import StaticTempSimulator
    return TempKeeper(StaticTempSimulator(), 100)
