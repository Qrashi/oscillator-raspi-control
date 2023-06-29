"""
Files to handle display interactions
"""

from .smart_display import SmartDisplay
from singlejson import load

"""
SmartDisplay: an non-stable API to display complicated texts, menus, animations on a DisplayModule
DisplayModule: a very simple "protocol" / "interface" to display text - static
"""


def init() -> SmartDisplay:
    """
    Get the correct SmartDisplay object
    :return:
    """
    if load("device.json", default={"device_type": "pc"}).json["device_type"] == "pi":
        from .modules.raspi_2004_lcd import Raspi_2004_lcd
        return SmartDisplay(Raspi_2004_lcd())
    from .modules.command_line import CommandLineDisplay
    return SmartDisplay(CommandLineDisplay())
