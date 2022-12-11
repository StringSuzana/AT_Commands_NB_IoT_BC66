import time
from dataclasses import dataclass

import serial as serial


@dataclass
class Sender:
    def sendAtCommand(self, ser: serial, command):
        ser.write((command + '\r').encode('ASCII'))
        time.sleep(1)
