from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ResponseStatus import Status


@dataclass
class AtResponse:
    status: Status
    response: List[str]
    wanted_params: dict
