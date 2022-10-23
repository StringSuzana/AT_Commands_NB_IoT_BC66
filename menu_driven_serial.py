from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
from pyfiglet import Figlet

import json
import string
import os
import binascii


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

    custom_fig = Figlet(font='standard')
    print(custom_fig.renderText('Nb-IoT BC66NA'))
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
