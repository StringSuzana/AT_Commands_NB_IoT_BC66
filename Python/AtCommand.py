from __future__ import annotations

from dataclasses import dataclass
from typing import List

from AtResponse import AtResponse, Param
from ResponseStatusEnum import Status


@dataclass
class AtCommand:
    command: str
    description: str
    expected_responses: List[AtResponse]
    read_response_method: ()  # read content of response message
    long_description: str = ""
    max_wait_for_response: int = 1  # [s]

    def replaceParamInCommand(self, param: str, value: str):
        self.command = self.command.replace(param.strip(), value.strip())
        return self
    def __post_init__(self):
        #add this to each command
        self.expected_responses.append(AtResponse(Status.ERROR, response=["+CME ERROR:<err>"], wanted=[Param(name="<err>")]))
