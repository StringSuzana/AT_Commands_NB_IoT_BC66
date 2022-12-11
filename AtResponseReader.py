from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List

from ArrayUtils import findIndex
from AtCommand import AtCommand
from AtResponse import AtResponse, Param
from ResponseStatus import Status


@dataclass
class Read:
    curren_response: str = ""
    at_response = []
    at_status = Status.WAITING
    at_expected_response: AtResponse = None

    def atResponse(self, serial, at_command_obj: AtCommand):
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

        for expected_response in at_command_obj.expected_responses:
            if self.checkIfMessageIsWhole(for_status=expected_response.status, expected=expected_response.response, given=response_array):
                self.at_expected_response = expected_response
                return
        self.at_status = Status.WAITING
        return

    def checkIfMessageIsWhole(self, for_status, expected, given) -> bool:
        # Check if the arrays have the same length
        if len(expected) != len(given):
            return False
        at_response_temp = []
        # Check if the elements of the arrays are the same
        for i in range(len(expected)):
            if expected[i] == given[i]:
                at_response_temp.append(given[i])
                continue
            else:
                if ":" in expected[i]:
                    # Check if the elements are both strings that start with "+Q_SOMETHING:"
                    if given[i].startswith(expected[i][:expected[i].index(":")]):
                        at_response_temp.append(given[i])
                        continue
                    # If the elements are not similar, return False
                    else:
                        return False
                # If this is not a row with +QAT: response, return False
                else:
                    return False

        if not at_response_temp:
            self.at_response = [Status.ERROR.name]
        else:
            self.at_response = at_response_temp

        self.at_status = for_status
        return True

    '''
    Below are methods for referencing in At commands
    in read_response_method property
    '''

    @staticmethod
    def answer(result_status: Status, result_array: List[str], at_expected_response: AtResponse):
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
    def answerWithWantedParams(result_status: Status, result_array: List[str], at_expected_response: AtResponse):
        if (len(result_array) == 0) | (len(at_expected_response.wanted) == 0):
            print(f"There is nothing to read")
            return AtResponse(status=result_status, response=result_array, wanted=[])
        else:
            print(f"AT STATUS: {result_status}\nRESPONSE: {result_array}")
            wanted_params = []

            for wanted in at_expected_response.wanted:
                row = wanted.response_row
                response_row = Read.getResponseRowFrom_Array(arr=result_array, row=row)
                expected_row = Read.getResponseRowFrom_Array(arr=at_expected_response.response, row=row)

                param_index = findIndex(arr=expected_row, element=wanted.name)
                if param_index != -1:
                    res = Param(name=wanted.name, value=response_row[param_index])
                    wanted_params.append(res)

            return AtResponse(status=result_status, response=result_array, wanted=wanted_params)

    @staticmethod
    def getResponseRowFrom_Array(arr, row):
        response_row = arr[row].replace(':', ',').split(',')
        return response_row
