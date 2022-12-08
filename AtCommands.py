from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List

from AtConstants import *

from ResponseStatus import Status


@dataclass
class AtResponse:
    status: Status
    response: List[str]
    wanted_params: dict


@dataclass
class AtCommand:
    command: str
    description: str
    expected_responses: List[AtResponse]
    read_response_method: ()  # read content of response message
    long_description: str = ""
    max_wait_for_response: int = 1  # [s]


@dataclass
class Read:
    curren_response: str = ""
    at_response = []
    at_status = Status.WAITING

    def atResponse(self, serial, at_command_obj: AtCommand):
        # TODO: READ FROM SERIAL
        # whole_msg_read = "OK\n+QAT:9,9,'I',,49\r"

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


at_read_ati = AtCommand(command=ATI, description="Display Product Identification Information.",
                        read_response_method=Read.answer,
                        expected_responses=[AtResponse(Status.OK, response=["Quectel_Ltd", "Quectel_BC66NA",
                                                                            "Revision: BC66NBR01A01:<revision>", "OK"],
                                                       wanted_params={"revision": ""}),
                                            AtResponse(Status.ERROR, response=["ERROR"], wanted_params={})],
                        max_wait_for_response=1)

at_read_operator_selection = AtCommand(command=AT_READ_OPERATOR_SELECTION, description="Read selected operator.",
                                       read_response_method=Read.answer,
                                       expected_responses=[
                                           AtResponse(Status.OK, response=["+COPS:<mode>,<format>,<oper>,<AcT>", "OK"], wanted_params={}),
                                           AtResponse(Status.ERROR, response=["ERROR"], wanted_params={})
                                       ],
                                       max_wait_for_response=1)

at_write_full_phone_functionality = AtCommand(command=AT_WRITE_FULL_PHONE_FUNCTIONALITY,
                                              description="Select FULL functionality in the MT (Mobile Termination).",
                                              long_description="This Write Command selects the level of functionality in the MT. "
                                                               "Level Full_functionality (1) is where the highest level of power is drawn. "
                                                               "Minimum_functionality (0) is where minimum power is drawn."
                                                               "Additionally available: "
                                                               "(4) Disable RF transmitting and receiving &"
                                                               "(7) Disable USIM only. RF transmitting and receiving circuits are still active.",
                                              read_response_method=Read.answer,
                                              expected_responses=[
                                                  AtResponse(Status.OK,
                                                             response=["OK"], wanted_params={}),
                                                  AtResponse(Status.ERROR, response=["ERROR"], wanted_params={})],
                                              max_wait_for_response=85)

at_write_old_scrambling_algorithm = AtCommand(command=AT_WRITE_OLD_SCRAMBLING_ALGORITHM,
                                              description="Select old scrambling code.",
                                              long_description="Used for selecting new or old scrambling code. "
                                                               "This is because code has been updated by 3GPPP,"
                                                               " and UE needs to select correct code for network.",
                                              read_response_method=Read.answer,
                                              expected_responses=[
                                                  AtResponse(Status.OK,
                                                             response=["+QSPCHSC: (list of supported <mode>s)", "OK"], wanted_params={}),
                                                  AtResponse(Status.ERROR, response=["ERROR"], wanted_params={})],
                                              max_wait_for_response=1)
at_write_eps_status_codes = AtCommand(command=AT_WRITE_EPS_STATUS_CODES,
                                      description="Write URC for EPS Network Registration Status.",
                                      long_description="This Write Command configures the different unsolicited result codes for "
                                                       "EPS Network Registration Status.",
                                      read_response_method=Read.answer,
                                      expected_responses=[
                                          AtResponse(Status.OK, response=[
                                              "+CEREG:<n>,<stat>,<tac>,<ci>,<AcT>,<cause_type>,<reject_cause>,<Active-Time>,<Periodic-TAU>",
                                              "OK"], wanted_params={}),
                                          AtResponse(Status.ERROR, response=["ERROR"], wanted_params={})],
                                      max_wait_for_response=1)

at_write_turn_off_psm = AtCommand(command=AT_WRITE_TURN_OFF_PSM, description="Turn off Power Saving Mode.",
                                  long_description="This Write Command controls the setting of the UE's power saving mode (PSM) parameters."
                                                   "It controls whether the UE wants to apply PSM or not, as well as the"
                                                   " requested extended periodic TAU value in E-UTRAN and the requested Active Time value.",
                                  read_response_method=Read.answer,
                                  expected_responses=[
                                      AtResponse(Status.OK, response=["OK"], wanted_params={}),
                                      AtResponse(Status.ERROR, response=["ERROR"], wanted_params={})],
                                  max_wait_for_response=1)

at_write_connection_status_enable_urc = AtCommand(command=AT_WRITE_CONNECTION_STATUS_URC,
                                                  description="This Write Command controls the presentation of an URC.",
                                                  long_description="This Write Command controls the presentation of an URC. "
                                                                   "If you write <n>=1, "
                                                                   "then  +CSCON: <mode> is sent from the MT (Mobile Termination) when the "
                                                                   "connection mode of the MT is changed.",
                                                  read_response_method=Read.answer,
                                                  expected_responses=[
                                                      AtResponse(Status.OK, response=["OK"], wanted_params={}),
                                                      AtResponse(Status.ERROR, response=["ERROR"], wanted_params={})],
                                                  max_wait_for_response=1)

at_read_connection_status = AtCommand(command=AT_READ_CONNECTION_STATUS,
                                      description="TA’s perceived radio connection status to the base station.",
                                      long_description="Read details of the TA’s perceived radio connection status to the base station. "
                                                       "Response is an indication of the current state <mode> 0=idle, 1=connected. "
                                                       "This state is only updated when radio events (sending and receiving) take place",
                                      read_response_method=Read.answer,
                                      expected_responses=[
                                          AtResponse(Status.OK, response=["+CSCON:<n>,<mode>", "OK"], wanted_params={}),
                                          AtResponse(Status.ERROR, response=["ERROR"], wanted_params={})],
                                      max_wait_for_response=1)

at_write_enable_wakeup_indication = AtCommand(command=AT_WRITE_ENABLE_WAKEUP_INDICATION,
                                              description="Enable Wakeup indication",
                                              read_response_method=Read.answer,
                                              expected_responses=[
                                                  AtResponse(Status.OK, response=["OK"], wanted_params={}),
                                                  AtResponse(Status.ERROR, response=["ERROR"], wanted_params={})],
                                              max_wait_for_response=1)

at_read_is_wakeup_indication_enabled = AtCommand(command=AT_READ_IS_WAKEUP_INDICATION_ENABLED,
                                                 description="Read if wakeup indication is enabled",
                                                 read_response_method=Read.answer,
                                                 expected_responses=[
                                                     AtResponse(Status.OK, response=["+QATWAKEUP: <enable>", "OK"], wanted_params={}),
                                                     AtResponse(Status.ERROR, response=["ERROR"], wanted_params={})],
                                                 max_wait_for_response=1)

AT_INITIAL_SETUP_SEQUENCE = [AT_WRITE_FULL_PHONE_FUNCTIONALITY, AT_WRITE_OLD_SCRAMBLING_ALGORITHM,
                             AT_WRITE_TURN_OFF_PSM, AT_WRITE_CONNECTION_STATUS_URC, AT_WRITE_ENABLE_WAKEUP_INDICATION,
                             AT_WRITE_OPERATOR_SELECTION, AT_EXECUTE_EXTENDED_SIGNAL_QUALITY, AT_READ_SIGNALING_STATUS,
                             AT_READ_OPERATOR_SELECTION, AT_WRITE_ATTACHED_STATE_GPRS]

AT_BASIC_INFO_SEQUENCE = [at_read_ati, at_read_operator_selection]
AT_OPEN_SOCKET_SEQUENCE = []
AT_SEND_UDP_MESSAGE_SEQUENCE = []
