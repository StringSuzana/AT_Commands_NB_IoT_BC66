from PyInquirer import prompt
from pyfiglet import Figlet
from datetime import datetime
import time
import string
import serial as serial

from AtCommands import AT_BASIC_INFO_SEQUENCE, AT_OPEN_SOCKET_SEQUENCE, AT_SEND_UDP_MESSAGE_SEQUENCE, TEMP_AT_MAKE_CONNECTION
from AtResponse import AtResponse
from AtResponseReader import Read
from Config import Server
from LogWriter import Write
from Menu import MessageValidator, MenuStyle


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

    def sendAtCommand(self, command):
        ser.write((command + '\r').encode('ASCII'))
        time.sleep(1)

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
        Don't use that execute loop
        rather switch to checking responses and deciding what to execute next
        """
        response = self.executeAtCommandSequence(TEMP_AT_MAKE_CONNECTION)
        return response

    def getNbIotModuleInfo(self) -> str:
        response = self.executeAtCommandSequence(AT_BASIC_INFO_SEQUENCE)
        return response

    def executeAtCommandSequence(self, sequence) -> string:
        whole_response = ''
        for i, at in enumerate(sequence):
            cmd_and_descr = f'\n{(i + 1):<3} | {at.command:.<20} |>>| {at.description}\n'
            print(cmd_and_descr)
            self.sendAtCommand(at.command)
            whole_response += cmd_and_descr
            at_response: AtResponse = Read().atResponse(serial=ser, at_command_obj=at)
            if at_response is not None:
                whole_response += f'>>{"RESPONSE:":>4}{",".join(at_response.response)}\n'
                whole_response += f'>>STATUS:{at_response.status}\n'

                if len(at_response.wanted) != 0:
                    for param in at_response.wanted:
                        wanted_param = f">>WANTED PARAM: {param.name} : {param.value}\n"
                        whole_response += wanted_param
                        print(wanted_param)
        return whole_response


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
        pass
        # sendMessageToServer(answers['message_text'])
    elif answers.get('nb_iot_main_menu') == '2':
        pass
        # sendTestMessageToServer()
    elif answers.get('nb_iot_main_menu') == '1':
        Write.toUniversalFile("".join(NbIoTSender().getNbIotModuleInfo()))
