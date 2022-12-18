from enum import Enum


class SocketStatus(Enum):
    INITIAL = 0,
    CONNECTING = 1,
    CONNECTED = 2,
    CLOSING = 3,
    REMOTE_CLOSING = 4
