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
AT_WRITE_SM_LOCK = 'AT+SM=LOCK'  # => Cemu ovo sluzi? maknuti
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


def getServerInfo():
    pass


def getAtCommandSequence():
    pass


def sendMessageToServer(message_text):
    pass


def sendTestMessageToServer():
    # get parameters from Nb Iot
    basic_info = getBasicInfo()
    sendMessageToServer(basic_info)


def getBasicInfo() -> string:
    response = ''
    sendAtCommand(ATI)
    response += readAtResponse()
    sendAtCommand(AT_READ_OPERATOR_SELECTION)
    response += readAtResponse()
    return response


def sendAtCommand(command):
    ser.write((command + '\r').encode('ASCII'))
    time.sleep(1)


def readAtResponse() -> string:
    out = ''
    while ser.in_waiting > 0:
        out += ser.read(1).decode('ASCII')
    if out != '':
        print(">> " + out)
    return datetime.now().strftime("%d-%m-%Y, %H:%M:%S") + " |   " + out + '=====================|\r'


def establishSerialConnection() -> bool:
    global ser
    ser = serial.Serial(port="COM10", baudrate=9600, timeout=301)
    while not ser.isOpen():
        print('.')
        continue
    return ser.isOpen()


def writeLinesToLogFile(text):
    with open(file='logs/at_log.txt', mode='a', encoding='ASCII') as f:
        text = text.replace('\r\n', '\r')
        f.write(text)


class MessageValidator(Validator):
    def validate(self, document):
        ok = True
        # Check for invalid characters
        # print(document.text)
        if not ok:
            raise ValidationError(message='Invalid message.', cursor_position=len(document.text))


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
        sendMessageToServer(answers['message_text'])
    elif answers.get('nb_iot_main_menu') == '2':
        sendTestMessageToServer()
    elif answers.get('nb_iot_main_menu') == '1':
        basicInfo = getBasicInfo()
        writeLinesToLogFile(basicInfo)
