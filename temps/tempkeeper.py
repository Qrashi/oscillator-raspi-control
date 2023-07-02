from .base_module import TemperatureProvider

import threading
from time import sleep


class TempKeeper:
    temp: float
    provider: TemperatureProvider
    interval: float

    def __init__(self, provider: TemperatureProvider, interval: float):
        self.provider = provider
        self.interval = interval
        threading.Thread(target=self.monitor, args=()).start()

    def get(self) -> float:
        return self.temp

    def monitor(self):
        while True:
            self.update()
            sleep(self.interval)

    def update(self):
        self.temp = self.provider.get()
