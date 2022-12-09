from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ResponseStatus import Status


@dataclass
class Param:
    name: str
    index: int
    value: str = ""
    response_row = 0


@dataclass
class AtResponse:
    status: Status
    response: List[str]
    wanted: List[Param]
