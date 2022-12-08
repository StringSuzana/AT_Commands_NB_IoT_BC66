from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List

from AtCommand import AtCommand
from AtResponse import AtResponse
from ResponseStatus import Status


@dataclass
class Read:
    curren_response: str = ""
    at_response = []
    at_status = Status.WAITING

    def atResponse(self, serial, at_command_obj: AtCommand):
        serial_msg = Read.fromSerial(serial)
        wait_intervals = at_command_obj.max_wait_for_response

        while (self.at_status == Status.WAITING) & (wait_intervals >= 0):
            self.parseMessage(at_command_obj, serial_msg)
            serial_msg = Read.fromSerial(serial)
            wait_intervals -= 1  # I want to sleep only 1 second at a time
            time.sleep(1)
        return at_command_obj.read_response_method(self.at_status, self.at_response)

    @staticmethod
    def fromSerial(serial) -> str:  # Make it return AtResponse
        out = ''
        while serial.in_waiting > 0:
            out += serial.read(1).decode('ASCII')

        if out != '':
            print(">> " + out)
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
            if self.checkIfMessageIsWhole(expected_response.status, expected=expected_response.response,
                                          given=response_array):
                return
        self.at_status = Status.WAITING
        return

    def checkIfMessageIsWhole(self, status, expected, given) -> bool:
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

        self.at_status = status
        return True

    @staticmethod
    def answer(result_status: Status, result_array: List[str]):
        if result_status == Status.OK:
            result_array = [res for res in result_array if res != Status.OK.name]
            # In each method I know where exactly should information be in a given string
            if len(result_array) == 0:
                print(result_status.name)
            else:
                print(f"AT STATUS: {result_status}\nRESPONSE: {result_array}")
                return AtResponse(status=result_status, response=result_array, wanted_params={"wanted_param": "Value1"})
            # PARSE THE RESPONSE IF STATUS IS OK
            return AtResponse(status=result_status, response=result_array, wanted_params={"wanted_param": "Value1"})
        print(result_status.name)

    @staticmethod
    def readIpAddr(result_status: Status, result_array: List[str]):
        if result_status == Status.OK:
            result_array = [res for res in result_array if res != Status.OK.name]
            # tu hardcoded odgovor
            print(result_array)
            # PARSE THE RESPONSE IF STATUS IS OK
            return result_array
        print(result_status.name)

    @staticmethod
    def socketStatus(result_status: Status, result_array: List[str]):
        # Here comes hardcoded index of an answer
        return result_array

    @staticmethod
    def ipAddress(result_status: Status, result_array: List[str]):
        # Here comes hardcoded index of an answer
        return result_array

    @staticmethod
    def operatorSelection(result_status: Status, result_array: List[str]):
        # Here comes hardcoded index of an answer
        return result_array
