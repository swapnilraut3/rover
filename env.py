import json
import logging
import numpy as np


class Environment():
    def __init__(self, temperature, humidity, solar_flare, storm, area_map, terrain=None):
        self.temperature = temperature
        self.humidity = humidity
        self.solar_flare = solar_flare
        self.storm = storm
        self.area_map = np.array(area_map)
        self.terrain = terrain

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, value):
        self._humidity = value

    @property
    def solar_flare(self):
        return self._solar_flare

    @solar_flare.setter
    def solar_flare(self, value):
        self._solar_flare = value

    @property
    def storm(self):
        return self._storm

    @storm.setter
    def storm(self, value):
        self._storm = value

    @property
    def area_map(self):
        return self._area_map

    @area_map.setter
    def area_map(self, value):
        self._area_map = value

    @property
    def terrain(self):
        return self._terrain

    @terrain.setter
    def terrain(self, value):
        # if value == None:
        #     self._terrain = ''
        self._terrain = value

    def toDict(self):
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "solar-flare": self.solar_flare,
            "storm": self.storm,
            "terrain": self.terrain
        }
