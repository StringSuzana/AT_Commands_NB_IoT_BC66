from __future__ import annotations

import string
import time
from dataclasses import dataclass
from typing import List

from AtConstants import *

from ResponseStatus import Status


@dataclass
class AtResponse:
    status: Status
    response: List[str]


@dataclass
class AtCommand:
    command: str
    description: str
    expected_responses: List[AtResponse]
    read_response_method: ()  # read content of response message
    max_wait_for_response: int = 1  # [s] multiple of 1 seconds


@dataclass
class Read:
    curren_response: str = ""
    at_response = []
    at_status = Status.WAITING

    def atResponse(self, at_command_obj: AtCommand):
        whole_msg_read = "OK\n+QAT:9,9,'I',,49\r"
        # whole_msg_read = "\r"
        wait_intervals = at_command_obj.max_wait_for_response

        while (self.at_status == Status.WAITING) & (wait_intervals > 0):
            self.readString(at_command_obj, whole_msg_read)
            wait_intervals -= 1  # I want to sleep only 1 second at a time
            time.sleep(1)
        return at_command_obj.read_response_method(self.at_status, self.at_response)

    def readString(self, at_command_obj: AtCommand, string_from_serial: str):
        if not string_from_serial:
            return
        # determine if it is done
        self.curren_response += string_from_serial
        response_array = self.curren_response.splitlines()
        response_array = [el for el in response_array if el != '']
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
            # tu hardcoded odgovor
            print(result_array)
            # PARSE THE RESPONSE IF STATUS IS OK
            return result_array
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


at_read_ati = AtCommand(command=ATI, description="Display Product Identification Information",
                        read_response_method=Read.answer,
                        expected_responses=[AtResponse(Status.OK, response=["Quectel_Ltd", "Quectel_BC66:<objectId>",
                                                                            "Revision: BC66NBR01A01:<revision>", "OK"]),
                                            AtResponse(Status.ERROR, response=["ERROR"])],
                        max_wait_for_response=1)

at_read_operator_selection = AtCommand(command=AT_READ_OPERATOR_SELECTION, description="Read selected operator",
                                       max_wait_for_response=1, read_response_method=Read.responseStatus,
                                       expected_response="OK")

at_write_full_phone_functionality = AtCommand(command=AT_WRITE_FULL_PHONE_FUNCTIONALITY, description="",
                                              max_wait_for_response=85, read_response_method=Read.responseStatus,
                                              expected_response="OK")

at_write_old_scrambling_algorithm = AtCommand(command=AT_WRITE_OLD_SCRAMBLING_ALGORITHM, description="",
                                              max_wait_for_response=1, read_response_method=Read.responseStatus,
                                              expected_response="OK")

at_write_eps_status_codes = AtCommand(command=AT_WRITE_EPS_STATUS_CODES, description="",
                                      max_wait_for_response=1, read_response_method=Read.responseStatus,
                                      expected_response="OK")

at_write_turn_off_psm = AtCommand(command=AT_WRITE_TURN_OFF_PSM, description="",
                                  max_wait_for_response=1, read_response_method=Read.responseStatus,
                                  expected_response="OK")

at_write_connection_status_urc = AtCommand(command=AT_WRITE_CONNECTION_STATUS_URC, description="",
                                           max_wait_for_response=1, read_response_method=Read.responseStatus,
                                           expected_response="OK")

at_read_connection_status = AtCommand(command=AT_READ_CONNECTION_STATUS, description="",
                                      max_wait_for_response=1, read_response_method=None,
                                      expected_response="??")

at_write_enable_wakeup_indication = AtCommand(command=AT_WRITE_ENABLE_WAKEUP_INDICATION, description="",
                                              max_wait_for_response=1, read_response_method=Read.responseStatus,
                                              expected_response="OK")

AT_INITIAL_SETUP_SEQUENCE = [AT_WRITE_FULL_PHONE_FUNCTIONALITY, AT_WRITE_OLD_SCRAMBLING_ALGORITHM,
                             AT_WRITE_TURN_OFF_PSM, AT_WRITE_CONNECTION_STATUS_URC, AT_WRITE_ENABLE_WAKEUP_INDICATION,
                             AT_WRITE_OPERATOR_SELECTION, AT_EXECUTE_EXTENDED_SIGNAL_QUALITY, AT_READ_SIGNALING_STATUS,
                             AT_READ_OPERATOR_SELECTION, AT_WRITE_ATTACHED_STATE_GPRS]

AT_BASIC_INFO_SEQUENCE = [at_read_ati, at_read_operator_selection]
AT_OPEN_SOCKET_SEQUENCE = []
AT_SEND_UDP_MESSAGE_SEQUENCE = []
