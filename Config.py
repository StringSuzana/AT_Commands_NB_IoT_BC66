from dataclasses import dataclass


@dataclass
class Server:
    IP_ADDR = 'raspberry_ip'
    PORT = '4444'
    UDP = 'UDP'
    TCP = 'TCP'
