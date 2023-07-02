from ..base_module import TemperatureProvider

from subprocess import run, PIPE
import re


class RaspiTemp(TemperatureProvider):
    """
    Static temperature simulator - since temperature is really not that important
    """
    def get(self):
        return float(re.findall(r'temp=(\d*\.?\d*)', run("/usr/bin/vcgencmd measure_temp", shell=True, stdout=PIPE, stderr=PIPE).stdout.decode('utf-8'))[0])
