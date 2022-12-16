from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ResponseStatusEnum import Status


@dataclass
class Param:
    name: str
    value: str = ""
    response_row: int = 0


@dataclass
class AtResponse:
    status: Status
    response: List[str]
    wanted: List[Param]
