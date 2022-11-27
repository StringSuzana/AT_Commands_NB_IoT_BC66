from dataclasses import dataclass

from MenuDrivenSerial import Sender

# TODO rewrite to AtCommand objects
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


@dataclass
class AtCommand:
    command: str
    description: str
    read_response_method = Sender().readAtResponse()
    max_wait_for_response: int = 60  # in seconds
    should_read_response: bool = False

    def convertCommandToAscii(self):
        pass

    def convertCommandToBinary(self):
        pass


# TODO: Make just a list of objects, don't initialize here
AT_BASIC_INFO_SEQUENCE_CLASSES = [AtCommand(ATI, "Display Product Identification Information"),
                                  AtCommand(AT_READ_OPERATOR_SELECTION, "Read selected operator")]
AT_SEND_UDP_PACKET_SEQUENCE_CLASSES = []

AT_VERIFY_CONNECTION_TO_SERVER_CLASSES = [AtCommand(AT_READ_PDP_CTX, "Read pdp context."),
                                          AtCommand(AT_READ_SHOW_PDP_ADDRESS, "Show Ip address."), ]
