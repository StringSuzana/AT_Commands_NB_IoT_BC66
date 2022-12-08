from __future__ import annotations

from dataclasses import dataclass
from typing import List

from AtResponse import AtResponse


@dataclass
class AtCommand:
    command: str
    description: str
    expected_responses: List[AtResponse]
    read_response_method: ()  # read content of response message
    long_description: str = ""
    max_wait_for_response: int = 1  # [s]
