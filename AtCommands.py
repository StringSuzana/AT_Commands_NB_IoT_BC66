from __future__ import annotations

import time
from dataclasses import dataclass
from AtConstants import *

from ResponseStatus import Status


@dataclass
class AtResponse:
    status: Status
    response: dict


@dataclass
class AtCommand:
    command: str
    description: str
    read_response_method: ()  # read content of response message
    max_wait_for_response: int = 1  # [s] multiple of 1 seconds
    expected_response: str = ""


@dataclass
class Read:
    @staticmethod
    def atResponse(command: AtCommand, func) -> AtResponse:
        whole_msg_read = "SOMETHING SOMETHING OK"
        wait_intervals = command.max_wait_for_response
        result = Read.__responseStatus(whole_msg=whole_msg_read)

        while (result.status == Status.WAITING) & wait_intervals > 0:
            # read again
            time.sleep(1)
            result = Read.__responseStatus(whole_msg=whole_msg_read)
            wait_intervals -= 1

        return func(result)

    @staticmethod
    def responseStatus(result: AtResponse) -> AtResponse:
        # do string splitting
        return AtResponse(status=Status.OK, response={})

    @staticmethod
    def socketStatus(result: AtResponse) -> AtResponse:
        # do string splitting
        return AtResponse(status=Status.OK, response={})

    @staticmethod
    def ipAddress(result: AtResponse) -> AtResponse:
        # wait for ok then read answer
        return AtResponse(status=Status.OK, response={})

    @staticmethod
    def operatorSelection(result: AtResponse) -> AtResponse:
        return AtResponse(status=Status.OK, response={})

    @staticmethod
    def __responseStatus(whole_msg) -> AtResponse:
        if Read.__isMessageOk(whole_msg):
            return AtResponse(status=Status.OK, response={})
        if Read.__isMessageError(whole_msg):
            return AtResponse(status=Status.ERROR, response={})  # read error message with AT+QIGETERROR somewhere above
        else:
            return AtResponse(status=Status.WAITING, response={})  # Or got and answer +something without ok at the end

    @staticmethod
    def __isMessageOk(whole_msg) -> bool:
        return whole_msg.rstrip()[-2:].strip() == "OK"

    @staticmethod
    def __isMessageError(self, whole_msg) -> bool:
        return whole_msg.rstrip()[-5:].strip() == "ERROR"


at_read_ati = AtCommand(command=ATI, description="Display Product Identification Information",
                        max_wait_for_response=1, read_response_method=Read.socketStatus,
                        expected_response="OK")

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
