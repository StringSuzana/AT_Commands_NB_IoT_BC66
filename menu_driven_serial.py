from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
from pyfiglet import Figlet

import json
import string
import os
import binascii

AT_FULL_PHONE_FUNCTIONALITY = "AT+CFUN=1"
AT_OLD_SCRAMBLING_ALGORITHM = "AT+QSPCHSC=1"
AT_SET_APN = "AT*MCGDEFCONT='IP','iot.ht.hr'"
AT_RESET_MODULE = "AT+QRESET=1"
AT_SM_LOCK = "AT+SM=LOCK"
AT_TURN_OFF_PSM = "AT+CEREG=5"
AT_CONNECT_STATUS = "AT+CSCON=1"
AT_ENABLE_WAKEUP_INDICATION = "AT+QATWAKEUP=1"


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
    return "Basic info"


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
    print(answers)
    if answers.get('nb_iot_main_menu') == '3':
        sendMessageToServer(answers['message_text'])
    elif answers.get('nb_iot_main_menu') == '2':
        sendTestMessageToServer()
    elif answers.get('nb_iot_main_menu') == '1':
        print(getBasicInfo())
