from enum import Enum


class AccessMode(Enum):
    """Data access mode of socket services"""
    BUFFER_ACCESS = 0
    DIRECT_PUSH = 1
