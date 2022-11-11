from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
from pyfiglet import Figlet
from datetime import datetime
import time
import json
import string
import os
import binascii
import serial as serial

ATI = 'ATI'  # Display Product Identification Information
AT_WRITE_FULL_PHONE_FUNCTIONALITY = 'AT+CFUN=1'
AT_WRITE_OLD_SCRAMBLING_ALGORITHM = 'AT+QSPCHSC=1'
AT_WRITE_APN = 'AT*MCGDEFCONT="IP","iot.ht.hr"'
AT_RESET_MODULE = 'AT+QRESET=1'
AT_WRITE_TURN_OFF_PSM = 'AT+CEREG=5'
AT_WRITE_CONNECT_STATUS = 'AT+CSCON=1'
AT_WRITE_ENABLE_WAKEUP_INDICATION = 'AT+QATWAKEUP=1'
AT_WRITE_OPERATOR_SELECTION = 'AT+COPS=1,2,"21901"'
AT_EXECUTE_EXTENDED_SIGNAL_QUALITY = "AT+CESQ"
AT_READ_SIGNALING_STATUS = "AT+CSCON?"
AT_READ_OPERATOR_SELECTION = 'AT+COPS?'
AT_WRITE_ATTACHED_STATE_GPRS = 'AT+CGATT=1'

AT_WRITE_ACTIVATE_PDN_CTX = 'AT+QGACT=1,1,"iot.ht.hr"'  # Wrong cid?
# AT_WRITE_ATTACHED_STATE_GPRS
AT_TEST_EXTENDED_SIGNAL_QUALITY = 'AT+CESQ=?'
AT_READ_EPS_NETWORK_REGISTRATION_STATUS = 'AT+CEREG?'
AT_READ_PDP_CTX = 'AT+CGDCONT?'
AT_WRITE_ACTIVATE_PDN_CTX_SECOND = 'AT+QGACT=1,2,"iot.ht.hr"'
AT_READ_SHOW_PDP_ADDRESS = 'AT+CGPADDR?'

AT_BASIC_INFO_SEQUENCE = [ATI, AT_READ_OPERATOR_SELECTION, AT_READ_PDP_CTX, AT_READ_SHOW_PDP_ADDRESS]
AT_SEND_UDP_PACKET_SEQUENCE = []
AT_INITIAL_SETUP_SEQUENCE = []


class AtCommand:
    def __init__(self, command, description):
        self.command = command
        self.description = description

    def convertCommandToAscii(self):
        pass

    def convertCommandToBinary(self):
        pass


AT_BASIC_INFO_SEQUENCE_CLASSES = [AtCommand(ATI, "Display Product Identification Information"),
                                  AtCommand(AT_READ_OPERATOR_SELECTION, "Read selected operator")]


class Sender:
    def __init__(self):
        self.serverIpAddress = '20.234.113.19'
        self.serverPort = '4444'
        self.protocol = 'UDP'

    def sendTestMessageToServer(self):
        pass

    def getNbIotModuleInfo(self) -> string:
        response = self.executeAtCommandSequence(AT_BASIC_INFO_SEQUENCE_CLASSES)
        return response

    def executeAtCommandSequence(self, sequence) -> string:
        whole_response = ''
        for i, at in enumerate(sequence):
            print(f"\nIndex: {i} : Command: {at.command} |>>| {at.description}")
            self.sendAtCommand(at.command)
            whole_response += self.readAtResponse()

            while self.isMessageOk(whole_response) != True | self.isMessageError(whole_response) != True:
                whole_response += self.readAtResponse()
            print(f"Command {at.command} executed successfully.") if self.isMessageOk(whole_response) else print(
                f"Command {at.command} executed with error.")
        return whole_response

    def sendMessageToServer(message_text):
        pass

    def sendAtCommand(self, command):
        ser.write((command + '\r').encode('ASCII'))
        time.sleep(1)

    def sendTestMessageToServer(self):
        # get parameters from Nb Iot
        basic_info = self.getNbIotModuleInfo()
        self.sendMessageToServer(basic_info)

    def readAtResponse(self) -> string:
        out = ''
        while ser.in_waiting > 0:
            out += ser.read(1).decode('ASCII')

        if out != '':
            print(">> " + out)
            # return datetime.now().strftime("%d-%m-%Y, %H:%M:%S") + " |   " + out + '=====================|\r'
            return datetime.now().strftime("%d-%m-%Y, %H:%M:%S") + " |   " + out
        else:
            return ''

    def isMessageOk(self, whole_msg) -> bool:
        return whole_msg.rstrip()[-2:].strip() == "OK"

    def isMessageError(self, whole_msg) -> bool:
        return whole_msg.rstrip()[-5:].strip() == "ERROR"


class Write:
    @staticmethod
    def toUniversalFile(text):
        with open(file='logs/at_log.txt', mode='a', encoding='ASCII') as f:
            text = text.replace('\r\n', '\r')
            f.write(text)

    @staticmethod
    def toSeparateFile(text):
        with open(file=f'logs/at_log_{datetime.now().strftime("d_%m_%Y_%Hh%Mm")}.txt', mode='w', encoding='ASCII') as f:
            text = text.replace('\r\n', '\r')
            f.write(text)


class MessageValidator(Validator):
    def validate(self, document):
        ok = True
        # Check for invalid characters
        # print(document.text)
        if not ok:
            raise ValidationError(message='Invalid message.', cursor_position=len(document.text))


def establishSerialConnection() -> bool:
    global ser
    ser = serial.Serial(port="COM10", baudrate=9600, timeout=301)
    while not ser.isOpen():
        print('.')
        continue
    return ser.isOpen()


if __name__ == '__main__':
    style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#673AB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#2196f3 bold',
        Token.Question: '',
    })

    custom_fig = Figlet(font='ogre')  # larry3d #ogre
    print(custom_fig.renderText('N b - I o T'))
    questions = [
        {
            'type': 'list',
            'name': 'nb_iot_main_menu',
            'message': 'Select what you want to do:',
            'choices': ['1. Do you want to get basic info?',
                        '2. Do you want to send basic test message to server?',
                        '3. Do you want to send custom message?',
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
    answers = prompt(questions, style=style)

    establishSerialConnection()

    print(answers)
    if answers.get('nb_iot_main_menu') == '3':
        pass
        # sendMessageToServer(answers['message_text'])
    elif answers.get('nb_iot_main_menu') == '2':
        pass
        # sendTestMessageToServer()
    elif answers.get('nb_iot_main_menu') == '1':
        Write.toUniversalFile(Sender().getNbIotModuleInfo())
