from PyInquirer import prompt
from pyfiglet import Figlet
import string
import serial as serial

from AtCommand import AtCommand
from AtCommands import *
from AtResponse import AtResponse
from AtResponseReader import Read
from Config import Server
from LogWriter import Write
from Menu import MessageValidator, MenuStyle
from Sender import Sender


class SerialCommunication:
    @staticmethod
    def open() -> bool:
        global ser
        ser = serial.Serial(port="COM10", baudrate=9600, timeout=301)
        while not ser.isOpen():
            print('.')
            continue
        return ser.isOpen()


class NbIoTSender:
    def __init__(self):
        self.serverIpAddress = Server.IP_ADDR
        self.serverPort = Server.PORT
        self.protocol = Server.UDP
        self.wholeResponse = ''

    def sendMessageToServer(self, message_text):
        self.executeAtCommandSequence(AT_OPEN_SOCKET_SEQUENCE)
        # transform message into ...hex?
        self.executeAtCommandSequence(AT_SEND_UDP_MESSAGE_SEQUENCE)
        pass

    def sendTestMessageToServer(self):
        """get parameters from Nb Iot"""
        basic_info = self.getNbIotModuleInfo()
        self.sendMessageToServer(basic_info)

    def establishConnection(self) -> str:
        """
        | at_read_pdp_context_status,
        |---->>if status is active, deactivate:
        |-------- at_write_pdp_context_status_deactivate,
        |-------- at_read_pdp_context_status,
        |---->>else:
        |-------- at_write_pdp_context_status_activate,
        |-------- at_read_pdp_context_status,
        |-------- at_write_activate_pdn_ctx
        """
        cid_in_active_state = "1"

        self.resetWholeResponse()
        pdp_ctx_response: AtResponse = self.executeAtCommand(at_read_pdp_context_status, i=0)

        if len(pdp_ctx_response.wanted) != 0:
            cid = next(filter(lambda p: p.name == "<cid>", pdp_ctx_response.wanted))
            state = next(filter(lambda p: p.name == "<state>", pdp_ctx_response.wanted))
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


    def getNbIotModuleInfo(self) -> str:
        response = self.executeAtCommandSequence(AT_BASIC_INFO_SEQUENCE)
        return response


    def executeAtCommand(self, at: AtCommand, i: int = 0):
        Sender().sendAtCommand(ser=ser, command=at.command)
        at_response: AtResponse = Read().readAtResponse(serial=ser, at_command_obj=at)
        self.wholeResponse += self.makeTextFromResponse(at_command=at, at_response=at_response, i=i)
        return at_response


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


    def executeAtCommandSequence(self, sequence) -> string:
        whole_response = ''
        for i, at in enumerate(sequence):
            at_response: AtResponse = self.executeAtCommand(at)
            text_response = self.makeTextFromResponse(at_command=at, at_response=at_response, i=i)
            whole_response += text_response
        return whole_response


    def resetWholeResponse(self):
        self.wholeResponse = ''


if __name__ == '__main__':
    SerialCommunication.open()
    custom_fig = Figlet(font='ogre')  # larry3d #ogre
    print(custom_fig.renderText('N b - I o T'))
    questions = [
        {
            'type': 'list',
            'name': 'nb_iot_main_menu',
            'message': 'Select what you want to do:',
            'choices': ['1. Print basic info to serial',
                        '2. Send basic test message to server',
                        '3. Send custom message to server',
                        '4. Do connection sequence to server'
                        ],
            'filter': lambda val: val[0:1:]  # I want just the number
        },
        {
            'type': 'input',
            'name': 'message_text',
            'message': 'Write the custom message you wish to send.',
            'when': lambda answers: answers['nb_iot_main_menu'] == '3',
            'validate': MessageValidator
        }
    ]
    answers = prompt(questions, style=MenuStyle.basic)

    print(answers)
    if answers.get('nb_iot_main_menu') == '4':
        Write.toUniversalFile("".join(NbIoTSender().establishConnection()))
    if answers.get('nb_iot_main_menu') == '3':
        # sendMessageToServer(answers['message_text'])
        pass
    elif answers.get('nb_iot_main_menu') == '2':
        # sendTestMessageToServer()
        pass
    elif answers.get('nb_iot_main_menu') == '1':
        Write.toUniversalFile("".join(NbIoTSender().getNbIotModuleInfo()))
