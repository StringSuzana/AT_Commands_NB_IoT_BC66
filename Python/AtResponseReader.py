from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List

from ArrayUtils import findIndex
from ArrayUtils import containsStatus
from AtCommand import AtCommand
from AtResponse import AtResponse, Param
from ResponseStatusEnum import Status


@dataclass
class Read:
    curren_response: str = ""
    at_response = []
    at_status = Status.WAITING
    at_expected_response: AtResponse = None

    def readAtResponse(self, serial, at_command_obj: AtCommand) -> AtResponse:
        serial_msg = Read.fromSerial(serial)
        wait_intervals = at_command_obj.max_wait_for_response

        while (self.at_status == Status.WAITING) & (wait_intervals >= 0):
            self.parseMessage(at_command_obj, serial_msg)
            serial_msg = Read.fromSerial(serial)
            wait_intervals -= 1  # I want to sleep only 1 second at a time
            time.sleep(1)
        return at_command_obj.read_response_method(self.at_status, self.at_response, self.at_expected_response)

    @staticmethod
    def fromSerial(serial) -> str:  # Make it return AtResponse
        out = ''
        while serial.in_waiting > 0:
            out += serial.read(1).decode('ASCII')

        if out != '':
            # print(">> " + out)
            return out
        else:
            return ''

    def parseMessage(self, at_command_obj: AtCommand, string_from_serial: str):
        if not string_from_serial:
            return
        # determine if it is done
        self.curren_response += string_from_serial
        response_array = self.curren_response.splitlines()
        # Remove empty string elements and remove the command that was sent because we want to deal only with responses
        response_array = [el for el in response_array if (el != '') & (el != at_command_obj.command)]
        if len(response_array) == 0:
            return

        for expected in at_command_obj.expected_responses:
            if self.checkIfMessageIsWhole(for_status=expected.status, expected_answer=expected.response, received_answer=response_array):
                self.setResponseAndStatus(for_status=expected.status, expected_answer=expected.response, received_answer=response_array)
                self.at_expected_response = expected
                return
        self.at_status = Status.WAITING
        return

    def checkIfMessageIsWhole(self, for_status, expected_answer, received_answer) -> bool:
        if self.checkIfUrcIsPresent(for_status, expected_answer, received_answer):
            # remove from received_answer and print out urc
            pass

        if len(expected_answer) == len(received_answer):
            if containsStatus(for_status.name, received_answer) & self.isValidAnswerForGivenCommand(
                    for_status, expected_answer, received_answer):
                return True

        return False

    def checkIfUrcIsPresent(self, for_status, expected, received):
        #TODO
        return True

    def isValidAnswerForGivenCommand(self, for_status, expected_answer, received_answer):
        #TODO
        return True

    '''
    Below are met*hods for referencing in At commands
 
   in read_response_method property
    '''

    @staticmethod
    def answer(result_status: Status, result_array: List[str], at_expected_response: AtResponse) -> AtResponse:
        if result_status == Status.OK:
            # result_array = [res for res in result_array if res != Status.OK.name]
            if len(result_array) == 0:
                return AtResponse(status=result_status, response=result_array, wanted=[])
            else:
                print(f"AT STATUS: {result_status}\nRESPONSE: {result_array}")
                return AtResponse(status=result_status, response=result_array, wanted=[])
            # PARSE THE RESPONSE IF STATUS IS OK
        return AtResponse(status=result_status, response=result_array, wanted=[])

    @staticmethod
    def answerWithWantedParams(result_status: Status, result_array: List[str], at_expected_response: AtResponse) -> AtResponse:
        if len(result_array) == 0:
            print(f"There is nothing to read")
            return AtResponse(status=result_status, response=result_array, wanted=[])
        elif len(at_expected_response.wanted) == 0:
            # print(f"There is no wanted parameters")
            return AtResponse(status=result_status, response=result_array, wanted=[])
        else:
            # print(f"AT STATUS: {result_status}\nRESPONSE: {result_array}")
            wanted_params = []

            for wanted in at_expected_response.wanted:
                row = wanted.response_row
                response_row = Read.getResponseRowFrom_Array(arr=result_array, row=row)
                expected_row = Read.getResponseRowFrom_Array(arr=at_expected_response.response, row=row)

                param_index = findIndex(arr=expected_row, element=wanted.name)
                if param_index != -1:
                    res = Param(name=wanted.name, value=response_row[param_index], description=wanted.description)
                    wanted_params.append(res)

            return AtResponse(status=result_status, response=result_array, wanted=wanted_params)

    @staticmethod
    def getResponseRowFrom_Array(arr: list[str], row: int):
        response_row = arr[row].replace(':', ',').split(',')
        return response_row

    def setResponseAndStatus(self, for_status, expected_answer, received_answer):
        at_response_temp = []

        for row in range(len(expected_answer)):
            # if for example expected_answer response is OK and received_answer response is OK
            if expected_answer[row] == received_answer[row]:
                at_response_temp.append(received_answer[row])
                continue
            elif received_answer[row].startswith("+CME"):
                at_response_temp.append(received_answer[row])
            else:
                # This is for the case that expected_answer +ATCOMMAND: has parameters
                if ":" in expected_answer[row]:
                    # Check if the elements are both strings that start with "+ATCOMMAND:"
                    command_name_end_index = expected_answer[row].index(":")
                    response_command_name = expected_answer[row][:command_name_end_index]

                    if received_answer[row].startswith(response_command_name):
                        at_response_temp.append(received_answer[row])
                        continue

        if not at_response_temp:
            self.at_response = [Status.ERROR.name]
        else:
            self.at_response = at_response_temp

        self.at_status = for_status
