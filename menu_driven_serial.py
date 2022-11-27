from PyInquirer import style_from_dict, Token, prompt
from pyfiglet import Figlet
from datetime import datetime
import time
import string
import serial as serial

from LogWriter import Write
from Menu import MessageValidator, MenuStyle

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

AT_WRITE_ACTIVATE_PDN_CTX = 'AT+QGACT=1,1,"iot.ht.hr"'
# AT_WRITE_ATTACHED_STATE_GPRS
AT_TEST_EXTENDED_SIGNAL_QUALITY = 'AT+CESQ=?'
AT_READ_EPS_NETWORK_REGISTRATION_STATUS = 'AT+CEREG?'  # +CEREG: 0,1
AT_READ_PDP_CTX = 'AT+CGDCONT?'  # Read pdp context info. RESPONSE: +CGDCONT: 1,"IP","iot.ht.hr","10.157.140.5",0,0,0,,,,,,0,,0
AT_READ_SHOW_PDP_ADDRESS = 'AT+CGPADDR?'  # Read the Ip address. RESPONSE: +CGPADDR: 1,10.157.140.5
AT_READ_UE_IP_ADDRESS = 'AT+QIPADDR'  # Read Ip of a DEVICE +QIPADDR: 10.152.26.119 +QIPADDR: 127.0.0.1
# TCP/IP
# 188.252.207.207 KOMP
# 20.234.113.19 AZURE
AT_WRITE_OPEN_SOCKET_SERVICE = 'AT+QIOPEN=1,0,"UDP","20.234.113.19",4445,4445,0,0'  # contextID = 1, connectionid = 0, DIRECT PUSH MODE = 1
# lokalno na raspberry     AT+QIOPEN=1,0,"UDP","188.252.207.207",4444,4444,0,0
# AT_WRITE_OPEN_SOCKET_SERVICE = 'AT+QIOPEN=1,0,"UDP","20.234.113.19",4444,0,0,0' # contextID = 1, connectionid = 0, buffer = 1
# AT_WRITE_OPEN_SOCKET_SERVICE = 'AT+QIOPEN=1,0,"TCP","20.234.113.19",5555,0,1' # contextID = 1, connectionid = 0, DIRECT PUSH MODE = 1
# AT+QISEND=0,5,12345
# AT+QISENDEX=0,5,3132333435
AT_CLOSE_SOCKET = 'AT+QICLOSE=0'
AT_READ_SOCKET_STATE = 'AT+QISTATE=1,0'  # Query the connection status of socket service 0.
# AT+QISEND=,0          #queries whether the data has reached the server.
AT_GET_LAST_ERROR_DESCRIPTION = 'AT+QIGETERROR'
AT_BASIC_INFO_SEQUENCE = [ATI, AT_READ_OPERATOR_SELECTION, AT_READ_PDP_CTX, AT_READ_SHOW_PDP_ADDRESS]
AT_SEND_UDP_PACKET_SEQUENCE = []
AT_INITIAL_SETUP_SEQUENCE = [AT_WRITE_FULL_PHONE_FUNCTIONALITY, AT_WRITE_OLD_SCRAMBLING_ALGORITHM, AT_WRITE_APN,
                             AT_WRITE_TURN_OFF_PSM, AT_WRITE_CONNECT_STATUS, AT_WRITE_ENABLE_WAKEUP_INDICATION,
                             AT_WRITE_OPERATOR_SELECTION, AT_EXECUTE_EXTENDED_SIGNAL_QUALITY, AT_READ_SIGNALING_STATUS,
                             AT_READ_OPERATOR_SELECTION, AT_WRITE_ATTACHED_STATE_GPRS]


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
AT_SEND_UDP_PACKET_SEQUENCE_CLASSES = []

AT_VERIFY_CONNECTION_TO_SERVER_CLASSES = [AtCommand(AT_READ_PDP_CTX, "Read pdp context."),
                                          AtCommand(AT_READ_SHOW_PDP_ADDRESS, "Show Ip address."), ]


class Sender:
    def __init__(self):
        self.serverIpAddress = '20.234.113.19'  # TODO: REPLACE WITH NEW VM
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

    def isMessageResponse(self, whole_msg) -> bool:
        # When AFTER OK, it should display some message
        pass


def establishSerialConnection() -> bool:
    global ser
    ser = serial.Serial(port="COM10", baudrate=9600, timeout=301)
    while not ser.isOpen():
        print('.')
        continue
    return ser.isOpen()


if __name__ == '__main__':
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
