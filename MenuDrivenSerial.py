from PyInquirer import prompt
from pyfiglet import Figlet
from datetime import datetime
import time
import string
import serial as serial

from AtCommands import AT_BASIC_INFO_SEQUENCE_CLASSES, AT_OPEN_SOCKET_SEQUENCE, AT_SEND_UDP_MESSAGE_SEQUENCE
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

    def sendMessageToServer(self, message_text):
        self.executeAtCommandSequence(AT_OPEN_SOCKET_SEQUENCE)
        # trnsform message into ...hex?
        self.executeAtCommandSequence(AT_SEND_UDP_MESSAGE_SEQUENCE)
        pass

    def sendTestMessageToServer(self):
        # get parameters from Nb Iot
        basic_info = self.getNbIotModuleInfo()
        self.sendMessageToServer(basic_info)

    def sendAtCommand(self, command):
        ser.write((command + '\r').encode('ASCII'))
        time.sleep(1)

    def getNbIotModuleInfo(self) -> string:
        response = self.executeAtCommandSequence(AT_BASIC_INFO_SEQUENCE_CLASSES)
        return response

    def executeAtCommandSequence(self, sequence) -> string:
        whole_response = ''
        for i, at in enumerate(sequence):
            command_info = f'Index: {i} : Command: {at.command} |>>| {at.description}\r'
            print(command_info)
            whole_response += command_info

            self.sendAtCommand(at.command)
            whole_response += self.readAtResponse()

            while self.isMessageOk(whole_response) != True | self.isMessageError(whole_response) != True:
                whole_response += self.readAtResponse()
            print(f"Command {at.command} executed successfully.") if self.isMessageOk(whole_response) else print(
                f"Command {at.command} executed with error.")
        return whole_response

    def readAtResponse(self) -> str:  # Make it return AtResponse
        out = ''
        while ser.in_waiting > 0:
            out += ser.read(1).decode('ASCII')

        if out != '':
            print(">> " + out)
            return datetime.now().strftime("%d-%m-%Y, %H:%M:%S") + " |   " + out
        else:
            return ''

    def isMessageOk(self, whole_msg) -> bool:
        return whole_msg.rstrip()[-2:].strip() == "OK"

    def isMessageError(self, whole_msg) -> bool:
        #if error=> read description with AT+QIGETERROR
        return whole_msg.rstrip()[-5:].strip() == "ERROR"

    def isMessageResponse(self, whole_msg) -> bool:
        # When AFTER OK, it should display some message
        pass


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
    if answers.get('nb_iot_main_menu') == '3':
        pass
        # sendMessageToServer(answers['message_text'])
    elif answers.get('nb_iot_main_menu') == '2':
        pass
        # sendTestMessageToServer()
    elif answers.get('nb_iot_main_menu') == '1':
        Write.toUniversalFile(NbIoTSender().getNbIotModuleInfo())