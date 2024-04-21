import time

from PyInquirer import prompt
from pyfiglet import Figlet
import string
import serial as serial

import Config
from AccessModeEnum import AccessMode
from ArrayUtils import findFirstActivePdpContextInParams, findParamInArrayByRow, findParamInArray, findParamInArrayByValue, \
    findParamsInArray
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
        ser = serial.Serial(port="COM10", baudrate=9600, timeout=301)
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
        self.context_id = "1"
        self.wholeResponse = ''

    def resetWholeResponse(self):
        self.wholeResponse = ''

    def getNbIotModuleInfo(self) -> str:
        response = self.executeAtCommandSequence(AT_BASIC_INFO_SEQUENCE)
        return response

    def setVerboseErrors(self):
        self.executeAtCommand(at_write_enable_verbose_errors)
        return self.wholeResponse

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

        + at_write_turn_off_psm                                 | AT+CPSMS=0
        + at_write_enable_wakeup_indication                     | AT+QATWAKEUP=1
        + at_read_is_wakeup_indication_enabled                  | AT+QATWAKEUP?
        '''
        self.executeAtCommandSequence(
            [
                at_write_full_phone_functionality,

                at_write_turn_off_psm,  # TODO: TURN ON LATER!
                at_write_enable_wakeup_indication,
                at_read_is_wakeup_indication_enabled
            ])
        return self.wholeResponse

    def _networkRegistration(self) -> str:
        """
        Second step in initialization of the device
        Network registration

        """
        '''
        +at_read_operator_selection                             | AT+COPS?
        +at_execute_extended_signal_quality                     | AT+CESQ 
        +at_write_connection_status_enable_urc                  | AT+CSCON=1
        +at_write_operator_selection                            | AT+COPS=1,2,"21901"
        +at_read_operator_selection                             | AT+COPS?  (should be +COPS: 1,2,"21901",9 => 9 is E-UTRAN (NB-S1 mode))
        + at_write_eps_status_codes (can be saved to device)    | AT+CEREG=5
        + at_read_eps_status_codes                              | AT+CEREG?
        +at_write_attach_to_packet_domain_service               | AT+CGATT=1 (The state of PDP context activation, should be +CGATT: 1)
        +at_read_attach_to_packet_domain_service                | AT+CGATT? <state> 0 Detached, 1 Attached
        +at_read_connection_status                              | AT+CSCON? (should be +CSCON: 1,1) (<n>=1=> Enable URC +CSCON: <mode>, <mode>=1=>Connected)
        +at_read_signal_strength_level_and_bit_error_rate       | AT+CSQ (Reference values https://m2msupport.net/m2msupport/atcsq-signal-quality/)
        '''
        self.executeAtCommandSequence(
            [
                at_read_operator_selection,
                at_execute_extended_signal_quality,
                at_write_connection_status_enable_urc,
                at_write_operator_selection,
                at_read_operator_selection,
                at_write_eps_status_codes,
                at_read_eps_status_codes,
                at_write_attach_to_packet_domain_service,
                at_read_attach_to_packet_domain_service,
                at_read_connection_status,
                at_read_signal_strength_level_and_bit_error_rate
            ])

        return self.wholeResponse

    def defineAndActivatePdpContext(self):
        """
        Third step in initialization of the device
        Defining and activating PDP/PDN context

        """
        '''
        at_read_pdp_contexts                     | AT+CGDCONT?                      
        
        Define PDP context
        + at_write_create_pdp_context_set_apn            | AT+CGDCONT=1,"IP","iot.ht.hr"
        
        Display all contexts
        + at_read_pdp_contexts                   | AT+CGDCONT? >>RESPONSE:+CGDCONT: 1,"IP","iot.ht.hr","10.198.148.209",0,0,0,,,,,,0,,0
        
        Check status of PDP profiles. Display context id <cid> and state <state>    
        + at_read_pdp_context_statuses           | AT+CGACT? >>RESPONSE:+CGACT: 1,1,OK
        
        Activate PDP context
        + at_write_activate_pdn_ctx              | AT+QGACT=1,1,"iot.ht.hr"
        '''
        #:+CGDCONT: 1,"IP","iot.ht.hr","10.198.148.209",0,0,0,,,,,,0,,0,OK || <cid> :  1,  <PDP_type> : "IP", <APN> : "iot.ht.hr"
        all_pdp_contexts_response: AtResponse = self.executeAtCommand(at_read_pdp_contexts)
        if all_pdp_contexts_response.status == Status.ERROR:
            print("Error reading PDP contexts. EXIT")
            return

        apn: Param = findParamInArrayByValue(param_name="<APN>", arr=all_pdp_contexts_response.wanted, param_value='iot.ht.hr')
        cid: Param = findParamInArrayByRow(param="<cid>", arr=all_pdp_contexts_response.wanted, row=apn.response_row)

        all_pdp_context_status_response: AtResponse = self.executeAtCommand(at_read_pdp_context_statuses)  # +CGACT: 1,1,OK | <cid> <state>
        param: Param = findParamInArrayByValue(param_name="<cid>", arr=all_pdp_context_status_response.wanted, param_value=cid.value)
        status: Param = findParamInArrayByRow(param="<state>", arr=all_pdp_context_status_response.wanted, row=param.response_row)

        if status.value == "1":
            self.context_id = cid.value
            self.wholeResponse += f"|>>|...PDP context already activated, skipping pdp creation and activation. cid {cid.value}, apn {apn.value}, state {status.value}"
            pass
        else:
            create_pdp_context_response: AtResponse = self.executeAtCommand(at_write_create_pdp_context_set_apn)
            if create_pdp_context_response.status == Status.ERROR:
                self.wholeResponse += f"|>>|...Not able to create PDP context. Disabling all PDP contexts and resetting the device. All inactive PDP contexts will be deleted after reset."
                cids = findParamsInArray(param="<cid>", arr=all_pdp_context_status_response.wanted)
                for i, cid_param in enumerate(cids):
                    self.executeAtCommand(at_write_pdp_context_status_deactivate.replaceParamInCommand("<cid>", cid_param.value), i=i)
                    self.executeAtCommandWithoutRead(at_reset)
                    return

            self.executeAtCommand(at_read_pdp_contexts)
            self.executeAtCommand(at_read_pdp_context_statuses)
            self.executeAtCommand(at_write_activate_pdn_ctx)

        return self.wholeResponse

    def doInitialSetup(self) -> str:
        """
        First step: _initBasicFunctionalities(), Second step: _networkRegistration(), Third step: _defineAndActivatePdpContext()
        Decide on AT_RESET_MODULE after setup
        """
        self.resetWholeResponse()

        self._initBasicFunctionalities()
        self._networkRegistration()
        self.defineAndActivatePdpContext()

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
        at_read_socket_status       | AT+QISTATE=0,<contextID>
            if opened
                ok
            else
                at_open_socket      | AT+QIOPEN=1,0,"UDP",<IP_address>,<remote_port>,4444,<access_mode>,0
        '''
        self.resetWholeResponse()
        socket_status_response: AtResponse = self.executeAtCommand(
            at_read_socket_status.replaceParamInCommand("<contextID>", self.context_id))
        socket_state = findParamInArray("<socket_state>", socket_status_response.wanted)
        if socket_state.value == SocketStatus.CONNECTED:
            print(f"Socket connected for contextID {self.context_id}")
        else:
            # self.executeAtCommand(at_close_socket) #here is specified connectID
            # time.sleep(2)
            at_open_socket_command = at_open_socket.replaceParamInCommand("<IP_address>", Config.Server.IP_ADDR)
            at_open_socket_command = at_open_socket_command.replaceParamInCommand("<remote_port>", Config.Server.PORT)
            at_open_socket_command = at_open_socket_command.replaceParamInCommand("<access_mode>", str(AccessMode.DIRECT_PUSH.value))
            at_open_socket_command = at_open_socket_command.replaceParamInCommand("<contextID>", self.context_id)
            socket_open_response = self.executeAtCommand(at_open_socket_command)

        time.sleep(5)
        self.executeAtCommand(at_read_socket_status)

        return self.wholeResponse

    def readIpAddress(self):
        self.executeAtCommand(at_read_pdp_address)  # Read the Ip address. RESPONSE: +CGPADDR: 1,10.157.140.5
        self.executeAtCommand(at_read_ue_ip_address)  # Read Ip of a DEVICE +QIPADDR: 10.152.26.119 +QIPADDR: 127.0.0.1

    @staticmethod
    def resetDevice():
        Sender().sendAtCommand(ser=ser, command=at_reset.command)

    def executeAtCommand(self, at: AtCommand, i: int = 0):
        Sender().sendAtCommand(ser=ser, command=at.command)
        at_response: AtResponse = Read().readAtResponse(serial=ser, at_command_obj=at)
        self.wholeResponse += self.makeTextFromResponse(at_command=at, at_response=at_response, i=i)
        return at_response

    def executeAtCommandSequence(self, sequence):
        for i, at in enumerate(sequence):
            self.executeAtCommand(at, i)

    @staticmethod
    def executeAtCommandWithoutRead(at: AtCommand, i: int = 0):
        cmd_and_descr = f'\n{(i + 1):<3} | {at.command:.<20} |>>| {at.description}\n'
        print(cmd_and_descr)
        Sender().sendAtCommand(ser=ser, command=at.command)

    @staticmethod
    def makeTextFromResponse(at_command, at_response: AtResponse, i=0):
        whole_response = ''
        cmd_and_descr = f'\n{(i + 1):<3} | {at_command.command:.<20} |>>| {at_command.description}\n'
        whole_response += cmd_and_descr

        if at_response is not None:
            whole_response += f'>>{"RESPONSE:":>4}{",".join(at_response.response)}\n'
            whole_response += f'>>STATUS:{at_response.status}\n'

            if len(at_response.wanted) != 0:
                for param in at_response.wanted:
                    description_part = f" |>>| {param.description:<30}" if param.description else ""
                    wanted_param = f">>WANTED PARAM: {param.name} : {param.value}  {description_part}\n"
                    whole_response += wanted_param
        print(whole_response)
        return whole_response


def main_menu():
    while True:
        custom_fig = Figlet(font='ogre')  # larry3d #ogre
        print(custom_fig.renderText('N b - I o T'))
        questions = [
            {
                'type': 'list',
                'name': NB_IOT_MAIN_MENU,
                'message': 'Select what you want to do:',
                'choices': ['0. Enable verbose error codes',
                            '1. Print basic info to serial',
                            '2. Send basic test message to server',
                            '3. Send custom message to server',
                            '4. Do initial setup. (_initBasicFunctionalities(), _networkRegistration(),and _defineAndActivatePdpContext())',
                            '5. Read IP address',
                            '6. Reset device',
                            '7. Open socket',
                            '8. Define And Activate Pdp Context',
                            '9. Close the program'
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
        choice = answers.get(NB_IOT_MAIN_MENU)
        print(answers)
        if choice == '9':
            print("Exiting the menu.")
            break
        elif choice == '8':
            Write.toUniversalFile("".join(NbIoTSender().defineAndActivatePdpContext()))
        elif choice == '7':
            Write.toUniversalFile("".join(NbIoTSender().reopenSocket()))
        elif choice == '6':
            NbIoTSender().resetDevice()
        elif choice == '5':
            Write.toUniversalFile("".join(NbIoTSender().readIpAddress()))
        elif choice == '4':
            Write.toUniversalFile("".join(NbIoTSender().doInitialSetup()))
        elif choice == '3':
            message_text = answers.get('message_text')
            Write.toUniversalFile("".join(NbIoTSender().sendMessageToServer(message_text)))
        elif choice == '2':
            Write.toUniversalFile("".join(NbIoTSender().sendMessage()))
        elif choice == '1':
            Write.toUniversalFile("".join(NbIoTSender().getNbIotModuleInfo()))
        elif choice == '0':
            Write.toUniversalFile("".join(NbIoTSender().setVerboseErrors()))


if __name__ == '__main__':
    SerialCommunication.open()
    main_menu()

    # TODO: citanje asinkronih poruka
    # frekvencija slanja i frekvencija čitanja, apn...
