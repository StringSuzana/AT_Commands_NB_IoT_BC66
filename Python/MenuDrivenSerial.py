import time

from PyInquirer import prompt
from pyfiglet import Figlet
import string
import serial as serial
import binascii

import Config
from AccessModeEnum import AccessMode
from ArrayUtils import findParamInArray
from AtCommands import *
from AtResponse import AtResponse
from AtResponseReader import Read
from Config import Server
from LogWriter import Write
from Menu import MessageValidator, MenuStyle
from Sender import Sender
from SocketStatusEnum import SocketStatus

NB_IOT_MAIN_MENU = 'nb_iot_main_menu'


class SerialCommunication:
    @staticmethod
    def open() -> bool:
        global ser
        ser = serial.Serial(port="COM19", baudrate=9600, timeout=301)
        while not ser.isOpen():
            print('.')
            continue
        print(Read.fromSerial(serial=ser))
        return ser.isOpen()


class NbIoTSender:
    def __init__(self):
        self.serverIpAddress = Server.IP_ADDR
        self.serverPort = Server.PORT
        self.protocol = Server.UDP
        self.wholeResponse = ''

    def resetWholeResponse(self):
        self.wholeResponse = ''

    def getNbIotModuleInfo(self) -> str:
        response = self.executeAtCommandSequence(AT_BASIC_INFO_SEQUENCE)
        return response

    def sendMessageToServer(self, message_text: str) -> str:
        """
        Send custom message to server
        AT+QISENDEX=0,<send_length>,<hex_string>
        """
        self.resetWholeResponse()

        message_hex = message_text.encode('utf-8').hex()
        send_length = len(message_text.encode('utf-8'))

        at_send_hex_command = at_send_hex.replaceParamInCommand('<send_length>', str(send_length))
        at_send_hex_command = at_send_hex_command.replaceParamInCommand('<hex_string>', message_hex)
        self.executeAtCommand(at_send_hex_command)
        # self.executeAtCommand(at_read_last_error_code)
        return self.wholeResponse

    def _checkLastErrorMessage(self):
        error_message = self.executeAtCommand(at_read_last_error_code)

    def sendTestMessageToServer(self):
        """get parameters from Nb Iot"""
        basic_info = self.getNbIotModuleInfo()
        self.sendMessageToServer(basic_info)

    def _initBasicFunctionalities(self) -> str:
        """
        First step in initialization of the device
        """
        '''
        + at_write_full_phone_functionality                     | AT+CFUN=1
        + at_write_eps_status_codes (can be saved to device)    | AT+CEREG=5
        -/+                    at_write_turn_off_psm            | AT+CPSMS=0
        + at_write_connection_status_enable_urc                 | AT+CSCON=1
        + at_write_enable_wakeup_indication                     | AT+QATWAKEUP=1
        + at_read_is_wakeup_indication_enabled                  | AT+QATWAKEUP?
        '''
        self.executeAtCommandSequence(
            [
                at_write_full_phone_functionality,
                at_write_eps_status_codes,
                at_write_turn_off_psm,
                at_write_enable_wakeup_indication,
                at_read_is_wakeup_indication_enabled
            ])
        return self.wholeResponse

    def _initForConnection(self) -> str:
        """
        Second step in initialization of the device
        Initialize operator and activate
        """
        '''
        +at_write_connection_status_enable_urc              | AT+CSCON=1
        +at_write_operator_selection                        | AT+COPS=1,2,"21901"
            - AT_EXECUTE_EXTENDED_SIGNAL_QUALITY = "AT+CESQ"
        +at_read_connection_status                          | AT+CSCON? (should be +CSCON: 1,1)
        +at_read_operator_selection                         | AT+COPS?  (should be +COPS: 1,2,"21901",9 => 9 is E-UTRAN (NB-S1 mode))
        +at_write_attach_to_packet_domain_service           | AT+CGATT=1 (The state of PDP context activation, should be +CGATT: 1)
        '''
        self.executeAtCommandSequence(
            [
                at_write_attach_to_packet_domain_service,
                at_write_connection_status_enable_urc,
                at_write_operator_selection,
                at_read_connection_status,
                at_read_operator_selection
            ])

        return self.wholeResponse

    def doInitialSetup(self) -> str:
        """
        First step: initBasicFunctionalities(), Second step: initForConnection()
        Decide on AT_RESET_MODULE after setup
        """
        self.resetWholeResponse()

        self._initBasicFunctionalities()
        self._initForConnection()

        return self.wholeResponse

    def establishConnection(self) -> str:
        """
        Set PDP context and activate PDN
        """
        '''
        | at_read_pdp_context_status                        | AT+CGACT?
        |---->>if status is active, deactivate:
        |-------- at_write_pdp_context_status_deactivate    | AT+CGACT=0,1
        |-------- at_read_pdp_context_status                | AT+CGACT?
        |---->>else:
        |-------- at_write_pdp_context_status_activate      | AT+CGACT=1,<cid>
        |-------- at_read_pdp_context_status                | AT+CGACT?
        |-------- at_write_activate_pdn_ctx                 | AT+QGACT=1,1,"iot.ht.hr"
        '''
        cid_in_active_state = "1"

        self.resetWholeResponse()
        pdp_ctx_response: AtResponse = self.executeAtCommand(at_read_pdp_context_status, i=0)

        if len(pdp_ctx_response.wanted) != 0:
            cid = findParamInArray("<cid>", pdp_ctx_response.wanted)
            state = findParamInArray("<state>", pdp_ctx_response.wanted)
            all_cid = [c_id for c_id in pdp_ctx_response.wanted if cid.value == "<cid>"]
            if state.value == cid_in_active_state:
                self.executeAtCommand(at_write_pdp_context_status_deactivate.replaceParamInCommand("<cid>", cid.value), i=1)
                self.executeAtCommand(at_read_pdp_context_status, i=2)

            self.executeAtCommand(at_write_pdp_context_status_activate.replaceParamInCommand("<cid>", cid.value), i=3)
            self.executeAtCommand(at_read_pdp_context_status, i=4)
            activate_pdn_context_result = self.executeAtCommand(at_write_activate_pdn_ctx, i=5)
            if activate_pdn_context_result.status == Status.ERROR:
                print("Try connecting again")

        return self.wholeResponse

    def sendMessage(self) -> str:
        self.resetWholeResponse()
        self.executeAtCommand(at_send_hex_test)
        return self.wholeResponse

    def reopenSocket(self) -> str:
        """
        Open UDP socket
        """
        '''
        at_read_socket_status       | AT+QISTATE=1,0
            if opened
                at_close_socket     | AT+QICLOSE=0
            else
                at_open_socket      | AT+QIOPEN=1,0,"UDP",<IP_address>,<remote_port>,4444,<access_mode>,0
        '''
        self.resetWholeResponse()
        self.executeAtCommand(at_close_socket)
        time.sleep(2)
        self.executeAtCommand(at_read_socket_status)
        # connectID = findParamInArray("<connectID>", socket_status_response.wanted)
        # socket_state = findParamInArray("<socket_state>", socket_status_response.wanted)
        # if connectID.value == SocketStatus.CONNECTING | connectID.value == SocketStatus.CONNECTED:
        # socket_close_response = self.executeAtCommand(at_close_socket)

        at_open_socket_command = at_open_socket.replaceParamInCommand("<IP_address>", Config.Server.IP_ADDR)
        at_open_socket_command = at_open_socket_command.replaceParamInCommand("<remote_port>", Config.Server.PORT)
        at_open_socket_command = at_open_socket_command.replaceParamInCommand("<access_mode>", str(AccessMode.DIRECT_PUSH.value))
        socket_open_response = self.executeAtCommand(at_open_socket_command)

        time.sleep(5)
        self.executeAtCommand(at_read_socket_status)

        return self.wholeResponse

    def readIpAddress(self) -> str:
        # TODO
        AT_READ_SHOW_PDP_ADDRESS = 'AT+CGPADDR?'  # Read the Ip address. RESPONSE: +CGPADDR: 1,10.157.140.5
        AT_READ_UE_IP_ADDRESS = 'AT+QIPADDR'  # Read Ip of a DEVICE +QIPADDR: 10.152.26.119 +QIPADDR: 127.0.0.1

        pass

    def reset(self):
        Sender().sendAtCommand(ser=ser, command=at_reset.command)

    def executeAtCommand(self, at: AtCommand, i: int = 0):
        cmd_and_descr = f'\n{(i + 1):<3} | {at.command:.<20} |>>| {at.description}\n'
        print(cmd_and_descr)
        Sender().sendAtCommand(ser=ser, command=at.command)
        at_response: AtResponse = Read().readAtResponse(serial=ser, at_command_obj=at)
        self.wholeResponse += self.makeTextFromResponse(at_command=at, at_response=at_response, i=i)
        return at_response

    def executeAtCommandSequence(self, sequence) -> string:
        whole_response = ''
        for i, at in enumerate(sequence):
            at_response: AtResponse = self.executeAtCommand(at)
            # text_response = self.makeTextFromResponse(at_command=at, at_response=at_response, i=i)
            # whole_response += text_response
        return whole_response

    def makeTextFromResponse(self, at_command, at_response: AtResponse, i=0):
        whole_response = ''
        cmd_and_descr = f'\n{(i + 1):<3} | {at_command.command:.<20} |>>| {at_command.description}\n'
        whole_response += cmd_and_descr

        if at_response is not None:
            whole_response += f'>>{"RESPONSE:":>4}{",".join(at_response.response)}\n'
            whole_response += f'>>STATUS:{at_response.status}\n'

            if len(at_response.wanted) != 0:
                for param in at_response.wanted:
                    wanted_param = f">>WANTED PARAM: {param.name} : {param.value}\n"
                    whole_response += wanted_param
        print(whole_response)
        return whole_response


if __name__ == '__main__':
    SerialCommunication.open()
    custom_fig = Figlet(font='ogre')  # larry3d #ogre
    print(custom_fig.renderText('N b - I o T'))
    questions = [
        {
            'type': 'list',
            'name': NB_IOT_MAIN_MENU,
            'message': 'Select what you want to do:',
            'choices': ['1. Print basic info to serial',
                        '2. Send basic test message to server',
                        '3. Send custom message to server',
                        '4. Do initial setup. (If device is restarted)',
                        '5. Do connection sequence to server',
                        '6. Reset device',
                        '7. Open socket',
                        ],
            'filter': lambda val: val[0:1:]  # I want just the number
        },
        {
            'type': 'input',
            'name': 'message_text',
            'message': 'Write the custom message you wish to send.',
            'when': lambda answers: answers[NB_IOT_MAIN_MENU] == '3',
            'validate': MessageValidator
        }
    ]
    answers = prompt(questions, style=MenuStyle.basic)
    print(answers)
    if answers.get(NB_IOT_MAIN_MENU) == '7':
        Write.toUniversalFile("".join(NbIoTSender().reopenSocket()))
    elif answers.get(NB_IOT_MAIN_MENU) == '6':
        NbIoTSender().reset()
    elif answers.get(NB_IOT_MAIN_MENU) == '5':
        Write.toUniversalFile("".join(NbIoTSender().establishConnection()))
    elif answers.get(NB_IOT_MAIN_MENU) == '4':
        Write.toUniversalFile("".join(NbIoTSender().doInitialSetup()))
    elif answers.get(NB_IOT_MAIN_MENU) == '3':
        message_text = answers.get('message_text')
        Write.toUniversalFile("".join(NbIoTSender().sendMessageToServer(message_text)))
    elif answers.get(NB_IOT_MAIN_MENU) == '2':
        Write.toUniversalFile("".join(NbIoTSender().sendMessage()))
    elif answers.get(NB_IOT_MAIN_MENU) == '1':
        Write.toUniversalFile("".join(NbIoTSender().getNbIotModuleInfo()))
