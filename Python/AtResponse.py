from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ResponseStatusEnum import Status


@dataclass
class Param:
    name: str
    value: str = ""
    response_row: int = 0
    description: str = "" #TODO: implement?

    def __post_init__(self):
        #remove all quotes (sometimes answer comes in more quotes than it should)
        self.value = self.value.replace("'", "").replace('"', "")

        self.value = f"{self.value}"
        #print(f"Param created: {self.name}, with value: {self.value} and response_row: {self.response_row}")


@dataclass
class AtResponse:
    status: Status
    response: List[str]
    wanted: List[Param]
