from prompt_toolkit.validation import Validator, ValidationError
from PyInquirer import style_from_dict, Token, prompt
from dataclasses import dataclass


class MessageValidator(Validator):
    def validate(self, document):
        ok = True
        # Check for invalid characters
        # print(document.text)
        if not ok:
            raise ValidationError(message='Invalid message.', cursor_position=len(document.text))


@dataclass
class MenuStyle:
    basic = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#673AB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#2196f3 bold',
        Token.Question: '',
    })

