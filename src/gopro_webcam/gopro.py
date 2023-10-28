from enum import Enum, IntEnum
from ipaddress import IPv4Address
from pprint import pprint
from time import sleep
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

JsonDict = Dict[str, Any]


class State(Enum):
    UNKNOWN = "unknown"
    WEBCAM_ON = "on"
    WEBCAM_OFF = "off"
    SLEEP = "sleep"


class Bitrate(IntEnum):
    """Bitrate in MBPS"""

    ONE = 1000000
    TWO = 2000000
    FIVE = 5000000


class Resolution(IntEnum):
    SD = 480
    HD = 720
    FHD = 1080
    QHD = 1440


class Fov(IntEnum):
    WIDE = 0
    LINEAR = 4
    NARROW = 6


class GoProWebcam:
    START_PATH = "/gp/gpWebcam/START"
    STOP_PATH = "/gp/gpWebcam/STOP"
    SETTINGS_PATH = "/gp/gpWebcam/SETTINGS"
    STATUS_PATH = "/gp/gpControl/status"
    SLEEP_PATH = "/gp/gpControl/command/system/sleep"

    def __init__(self, ip: IPv4Address) -> None:
        self.ip = ip
        self._state = State.UNKNOWN

    def _make_request(self, route: str, params: Optional[JsonDict] = None) -> JsonDict:
        if self._state == State.SLEEP:
            print("GoPro is not on")
            return {}
        if self._state == State.UNKNOWN:
            print("GoPro current state is unknown, requests may timeout")

        url = urljoin(f"http://{self.ip}", route)
        try:
            response = requests.get(url, params=params, timeout=2)
            pprint(response.json())
            return response.json()
        except requests.exceptions.ConnectTimeout:
            print(f"requested {url} timed out")
        return {}

    def start(self) -> JsonDict:
        response = self._make_request(self.START_PATH)
        self._state = State.WEBCAM_ON
        return response

    def stop(self) -> JsonDict:
        response = self._make_request(self.STOP_PATH)
        self._state = State.WEBCAM_OFF
        return response

    def sleep(self) -> None:
        self._make_request(self.SLEEP_PATH)
        self._state = State.SLEEP

    def set_resolution(self, resolution: Resolution) -> JsonDict:
        params = {"res": resolution.value}
        return self._make_request(self.START_PATH, params)

    def set_fov(self, fov: Fov) -> JsonDict:
        params = {"fov": fov.value}
        return self._make_request(self.SETTINGS_PATH, params)

    def set_bitrate(self, bitrate: Bitrate) -> JsonDict:
        params = {"bitrate": bitrate.value}
        return self._make_request(self.SETTINGS_PATH, params)

    def get_status(self) -> JsonDict:
        return self._make_request(self.STATUS_PATH)


