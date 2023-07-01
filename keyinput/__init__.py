import singlejson
from singlejson import load

from .button_manager import ButtonManager


class KeyInputInstance:
    manager: ButtonManager = None


instance = KeyInputInstance()


def init() -> ButtonManager:
    if load("device.json", default={"device_type": "pc"}).json["device_type"] == "pi":
        from .modules.gpio import GPIOButtons
        instance.manager = ButtonManager(GPIOButtons())
        return instance.manager
    from .modules.command_line import CLIButtons
    instance.manager = ButtonManager(CLIButtons())
    return instance.manager


def end():
    """
    Terminate key-checking
    :return:
    """
    if instance.manager is None:
        return
    if instance.manager.button_module is None:
        return
    instance.manager.button_module.end()
