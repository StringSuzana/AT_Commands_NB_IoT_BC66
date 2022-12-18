from dataclasses import dataclass

from Secrets import Secrets


@dataclass
class Server:
    IP_ADDR = Secrets.IP_ADDR
    PORT = Secrets.PORT
    UDP = 'UDP'
    TCP = 'TCP'
