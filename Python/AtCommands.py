from __future__ import annotations

from AtCommand import AtCommand
from AtConstants import *
from AtResponse import AtResponse, Param
from AtResponseReader import Read
from ResponseStatusEnum import Status

'''
Info
'''
at_read_ati = AtCommand(
    command=ATI,
    description="Display Product Identification Information.",
    read_response_method=Read.answer,
    expected_responses=
    [
        AtResponse(
            Status.OK, response=["Quectel_Ltd", "Quectel_BC66NA", "Revision: BC66NBR01A01:<revision>", "OK"],
            wanted=[Param(name="<revision>")], ),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])
    ],
    max_wait_for_response=1)
at_read_imei = AtCommand(
    command=AT_READ_IMEI,
    description="Read IMEI",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=
    [
        AtResponse(
            Status.OK, response=["+CGSN:<IMEI>", "OK"],
            wanted=[Param(name="<IMEI>")], ),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])
    ],
    max_wait_for_response=1)
at_read_power_supply_voltage = AtCommand(
    command=AT_READ_POWER_SUPPLY_VOLTAGE,
    description="This command queries the voltage value of power supply",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=
    [
        AtResponse(
            Status.OK, response=["+CBC:<bcs>,<bcl>,<voltage>", "OK"],
            wanted=[Param(name="<bcs>"), Param(name="<bcl>"), Param(name="<voltage>"), ]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])
    ],
    max_wait_for_response=1)
at_read_signal_strength_level_and_bit_error_rate = AtCommand(
    command='AT+CSQ',
    description="This Execution Command returns the received signal strength level <rssi> "
                "and the channel bit error rate <ber> from the MT.",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=
    [
        AtResponse(
            Status.OK, response=["+CSQ:<rssi>,<ber>", "OK"],
            wanted=[Param(name="<rssi>"), Param(name="<ber>")]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[]),
        AtResponse(Status.ERROR, response=["+CME ERROR:<err>"], wanted=[Param(name="<err>")])
    ],
    max_wait_for_response=1)
'''
Basic Setup
'''
at_write_full_phone_functionality = AtCommand(
    command=AT_WRITE_FULL_PHONE_FUNCTIONALITY,
    description="AT+CFUN=1 Select FULL functionality in the MT (Mobile Terminal).",
    long_description=
    "This Write Command selects the level of functionality in the MT. "
    "Level Full_functionality (1) is where the highest level of power is drawn. "
    "Minimum_functionality (0) is where minimum power is drawn."
    "Additionally available: "
    "(4) Disable RF transmitting and receiving &"
    "(7) Disable USIM only. RF transmitting and receiving circuits are still active.",
    read_response_method=Read.answer,
    expected_responses=
    [
        AtResponse(Status.OK, response=["OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])
    ],
    max_wait_for_response=85)
'''
This is in old manual.
at_write_old_scrambling_algorithm = AtCommand(
    command=AT_WRITE_OLD_SCRAMBLING_ALGORITHM,
    description="AT+QSPCHSC=1 Select old scrambling code.",
    long_description="Used for selecting new or old scrambling code. "
                     "This is because code has been updated by 3GPPP,"
                     " and UE needs to select correct code for network.",
    read_response_method=Read.answer,
    expected_responses=
    [
        AtResponse(Status.OK, response=["+QSPCHSC: (list of supported <mode>s)", "OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])
    ],
    max_wait_for_response=5)
'''
at_write_eps_status_codes = AtCommand(
    command=AT_WRITE_EPS_STATUS_CODES,
    description="Write URC for EPS Network Registration Status.",
    long_description="This Write Command configures the different unsolicited result codes for "
                     "EPS Network Registration Status.",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(
            Status.OK, response=[
                "+CEREG:<n>,<stat>,<tac>,<ci>,<AcT>,<cause_type>,<reject_cause>,<Active-Time>,<Periodic-TAU>",
                "OK"], wanted=[]),
        AtResponse(
            Status.OK, response=["OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=1)

at_write_turn_off_psm = AtCommand(
    command=AT_WRITE_TURN_OFF_PSM, description="Turn off Power Saving Mode.",
    long_description="This Write Command controls the setting of the UE's power saving mode (PSM) parameters."
                     "It controls whether the UE wants to apply PSM or not, as well as the"
                     " requested extended periodic TAU value in E-UTRAN and the requested Active Time value.",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(Status.OK, response=["OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=1)

# When enabled, the answer +CSCON: 1 or 0 can come at any time there is a change in connection mode
#    TODO: write reader so that is checks if answer that came is in fact the connection status URC
#            OR think about not using the signaling, rather just query the AT+CSCON?

at_write_connection_status_enable_urc = AtCommand(
    command=AT_WRITE_CONNECTION_STATUS_URC,
    description="This Write Command controls the presentation of an URC.",
    long_description="This Write Command controls the presentation of an URC. "
                     "If you write <n>=1, "
                     "then  +CSCON: <mode> is sent from the MT (Mobile Termination) when the "
                     "connection mode of the MT is changed. Remains valid after deep-sleep wakeup. "
                     "The configuration will not be saved to NVRAM.",
    read_response_method=Read.answer,
    expected_responses=[
        AtResponse(Status.OK, response=["OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=1)

at_write_enable_wakeup_indication = AtCommand(
    command=AT_WRITE_ENABLE_WAKEUP_INDICATION,
    description="Enable Wakeup indication",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(Status.OK, response=["OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=1)

at_read_is_wakeup_indication_enabled = AtCommand(
    command=AT_READ_IS_WAKEUP_INDICATION_ENABLED,
    description="Read if wakeup indication is enabled",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(Status.OK, response=["+QATWAKEUP: <enable>", "OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=1)
'''
Setup connection
    AT_WRITE_OPERATOR_SELECTION = 'AT+COPS=1,2,"21901"'
    AT_EXECUTE_EXTENDED_SIGNAL_QUALITY = "AT+CESQ"
    AT_READ_CONNECTION_STATUS = "AT+CSCON?"
    AT_READ_OPERATOR_SELECTION = 'AT+COPS?'
    AT_WRITE_ATTACH_TO_PACKET_DOMAIN_SERVICE = 'AT+CGATT=1'

'''
at_write_operator_selection = AtCommand(
    command=AT_WRITE_OPERATOR_SELECTION,
    description="Manual operator selection (<oper> field shall be present)",
    long_description="21901 is Hrvatski Telekom."
                     "The command (AT+COPS=1,2,'21901')takes effect immediately."
                     "Remain valid after deep-sleep wakeup."
                     "The configurations will be saved to NVRAM.",
    read_response_method=Read.answer,
    expected_responses=[
        AtResponse(Status.OK, response=["OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=900)

at_execute_extended_signal_quality = AtCommand(
    command=AT_EXECUTE_EXTENDED_SIGNAL_QUALITY,
    description="This Execution Command returns received signal quality parameters.",
    long_description="The terminal will provide a current signal strength indicator of 0 to 99,"
                     " where a larger number indicates better signal quality."
                     "*** <rscp> and <ecno> are not applicable for NB-IoT network and should be set to "
                     "-not known- or -not detectable- (255) for BC66/BC66-NA modules. "
                     "*** the network quality can be evaluated according to a general rule as specified: "
                     "Strong: RSRP ≥ -100 dBm and RSRQ ≥ -7 dB. "
                     "Median: -100 dbm ≥ RSRP ≥ -110 dbm, and RSRQ ≥ -11 dB."
                     "<rsrp> Integer type. Reference signal received power (RSRP, see 3GPP 36.133). "
                     "When sending data is needed, RSRP is recommended to be greater than -115 dbm.",
    read_response_method=Read.answer,
    expected_responses=[
        AtResponse(
            Status.OK, response=["+CESQ: <rxlev>,<ber>,<rscp>,<ecno>,<rsrq>,<rsrp>", "OK"],
            wanted=[Param(name="<rxlev>", response_row=0),
                    Param(name="<ber>", response_row=0),
                    Param(name="<rscp>", response_row=0),
                    Param(name="<ecno>", response_row=0),
                    Param(name="<rsrq>", response_row=0),
                    Param(name="<rsrp>", response_row=0)]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=2)

at_read_connection_status = AtCommand(
    command=AT_READ_CONNECTION_STATUS,
    description="Terminal Adapter's (TA) perceived radio connection status to the base station.",
    long_description="AT+CSCON command gives details of the TA’s perceived radio connection status (i.e., to the base station). "
                     "It returns an indication of the current state. TA, or Terminal Adapter, is a term used to refer to a device "
                     "that connects a mobile terminal (MT) to the radio access network (RAN), allowing the MT to communicate with "
                     "the network and other devices.",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(Status.OK, response=["+CSCON:<n>,<mode>", "OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=1)

at_read_operator_selection = AtCommand(
    command=AT_READ_OPERATOR_SELECTION,
    description="Read selected operator.",
    long_description="AT+COPS?",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=
    [
        AtResponse(Status.OK, response=["+COPS:<mode>,<format>,<oper>,<AcT>", "OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])
    ],
    max_wait_for_response=900)

at_write_attach_to_packet_domain_service = AtCommand(
    command=AT_WRITE_ATTACH_TO_PACKET_DOMAIN_SERVICE,
    description="Attach the Mobile Terminal (MT) to the Packet Domain Service",
    long_description="This Write Command is used to attach the MT to, or detach the MT from, the packet domain service. After the "
                     "command has completed, the MT remains in V.250 command state. If the MT is already in the requested state, "
                     "the command will be ignored and the OK response will still be returned. If the requested state cannot be achieved,"
                     " an ERROR will be returned. Any active PDP contexts will be automatically deactivated when the attachment "
                     "state changes to detached. This Read Command returns the current packet domain service state. ",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(Status.OK, response=["OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=86)

at_reset = AtCommand(
    command='AT+QRST=1',
    description="Reset the device",
    read_response_method=Read.answer,
    expected_responses=[
        AtResponse(Status.OK, response=["OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=1)

'''
Enable PDP and connect to PDN sequence
'''
at_read_pdp_context_status = AtCommand(
    command=AT_READ_PDP_CONTEXT_STATE,
    description="Reads if (PDP) Packet Data Protocol context is activated. If It is, it should be deactivated before setting PDN",
    long_description="",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(
            Status.OK, response=["+CGACT:<cid>,<state>", "OK"], wanted=[Param(name="<cid>"), Param(name="<state>")]),
        AtResponse(
            Status.OK, response=["+CGACT:<cid>,<state>", "+CGACT:<cid>,<state>", "OK"],
            wanted=[Param(name="<cid>", response_row=0),
                    Param(name="<state>", response_row=0),
                    Param(name="<cid>", response_row=1),
                    Param(name="<state>", response_row=1)]),
        AtResponse(Status.OK, response=["NO CARRIER"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=150)

at_write_pdp_context_status_deactivate = AtCommand(
    command="AT+CGACT=0,<cid>",
    description="Deactivate PDN",
    long_description="AT+CGACT=<state>,<cid> state=0=deactivate",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(Status.OK, response=["OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=150)

at_write_pdp_context_status_activate = AtCommand(
    command="AT+CGACT=1,<cid>",
    description="Activate PDN",
    long_description="AT+CGACT=<state>,<cid> state=1=activate",
    read_response_method=Read.answer,
    expected_responses=[
        AtResponse(Status.OK, response=["OK"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=150)

at_write_activate_pdn_ctx = AtCommand(
    command=AT_WRITE_ACTIVATE_PDN_CTX,
    description="AT+QGACT command activates a specified PDN context",
    long_description="AT+QGACT=1,1,'iot.ht.hr' command connects to ip. "
                     "AT+QGACT=<op>,<PDP_type>,<APN>  is for activating"
                     "AT+QGACT=<op>,<cid>             is for deactivating",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        # this should not be possible because I will always deactivate PDP before activating a PDN context:
        # AtResponse(Status.OK, response=["+QGACT:<cid>,<type>,<result>,<activated_PDP_type>","OK"], wanted=[]),
        AtResponse(
            Status.OK, response=["+QGACT:<cid>", "OK", "+QGACT:<cid>,<type>,<result>,<activated_PDP_type>"],
            wanted=[Param(name="<cid>", response_row=1),
                    Param(name="<result>", response_row=1),
                    Param(name="<activated_PDP_type>", response_row=1)]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=1)

'''
Open and close Socket
>>> contextID = 1, connectID= 0, access_mode = DIRECT PUSH MODE = 1
AT+QIOPEN=<contextID>,<connectID>,<service_type>,<IP_address>,<remote_port>,<local_port>,<access_mode>,<protocol_type>
AT_WRITE_OPEN_SOCKET_SERVICE = 'AT+QIOPEN=1,0,"UDP","20.234.113.19",4445,4445,1,0' 

'''

at_open_socket = AtCommand(
    command='AT+QIOPEN=1,0,"UDP",<IP_address>,<remote_port>,5555,<access_mode>,0',
    description="This command is used to open a socket service. "
                "Provide: <IP_address>,<remote_port> and <access_mode>",
    long_description="The service type can be specified by <service_type>, "
                     "and the data access mode can be specified by <access_mode>. "
                     "The URC +QIOPEN:<connectID>,<err> will be reported to indicate whether the"
                     " socket service has been opened successfully."
                     "The command takes effect immediately.When a UDP session is created, the module can automatically "
                     "backup the latest UDP configurations, and the MCU can send/receive data directly after being woken up from sleep."
                     "IF ERROR: If the connection failed, AT+QICLOSE=<connectID> must be executed to close the socket",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(
            Status.OK, response=["OK", "+QIOPEN:<connectID>,<err>"],
            wanted=[Param(name="<connectID>", response_row=1),
                    Param(name="<err>", response_row=1)]),
        AtResponse(status=Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=60)

at_close_socket = AtCommand(
    command='AT+QICLOSE=0',
    description="AT+QICLOSE=<connectID> This command is used to close a socket service.",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(
            Status.OK, response=["OK", "CLOSE OK"],
            wanted=[]),
        AtResponse(status=Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=1)

at_read_socket_status = AtCommand(
    command='AT+QISTATE=1,0',
    description='AT+QISTATE=<query_type>,<connectID> Query the state of socket.',
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[AtResponse(
        Status.OK,
        response=["+QISTATE:<connectID>,<service_type>,<IP_address>,<remote_port>,<local_port>,<socket_state>,<contextID>,<access_mode>]",
                  "OK"],
        wanted=[
            Param(name="<connectID>", response_row=0),
            Param(name="<service_type>", response_row=0),
            Param(name="<IP_address>", response_row=0),
            Param(name="<remote_port>", response_row=0),
            Param(name="<local_port>", response_row=0),
            Param(name="<socket_state>", response_row=0),
            Param(name="<contextID>", response_row=0),
            Param(name="<access_mode>", response_row=0),
        ]),
        AtResponse(status=Status.OK, response=["OK"], wanted=[]),
        AtResponse(status=Status.ERROR, response=["ERROR"], wanted=[])
    ],
    max_wait_for_response=1
)
'''
Send messages
'''
at_send_hex_test = AtCommand(
    command='AT+QISENDEX=0,5,3132333435',
    description='AT+QISENDEX=<connectID>,<send_length>,<hex_string>. To send message',
    long_description='send_length= max length is 512 bytes.',
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(Status.OK, response=["OK", "SEND OK"], wanted=[]),
        AtResponse(Status.OK, response=["OK", "SEND FAIL"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])
    ],
    max_wait_for_response=2
)
at_send_hex = AtCommand(
    command='AT+QISENDEX=0,<send_length>,<hex_string>',
    description='AT+QISENDEX=<connectID>,<send_length>,<hex_string>. To send message',
    long_description='send_length= max length is 512 bytes.',
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(Status.OK, response=["OK", "SEND OK"], wanted=[]),
        AtResponse(Status.OK, response=["OK", "SEND FAIL"], wanted=[]),
        AtResponse(Status.ERROR, response=["ERROR"], wanted=[])
    ],
    max_wait_for_response=1
)

'''
Error codes
'''
at_read_last_error_code = AtCommand(
    command='AT+QIGETERROR',
    description="This command is used to query the <err> code and specific description "
                "of the <err> code returned by the last TCP/IP command",
    long_description="If response is ERROR, there is an error related to ME functionality:",
    read_response_method=Read.answerWithWantedParams,
    expected_responses=[
        AtResponse(
            Status.OK, response=["+QIGETERROR:<err>,<errcode_description>", "OK"],
            wanted=[Param(name="<err>", response_row=0),
                    Param(name="<errcode_description>", response_row=0)]),
        AtResponse(status=Status.ERROR, response=["ERROR"], wanted=[])],
    max_wait_for_response=1)

at_write_enable_verbose_errors = AtCommand(
    command='AT+CMEE=2',
    description="This command enables verbose error reporting. Enables +CME ERROR: <err> and description."
                "Remains valid after deep-sleep wakeup. "
                "Configuration will not be saved to NVRAM.",
    read_response_method=Read.answer,
    expected_responses=
    [
        AtResponse(
            Status.OK, response=["OK"],
            wanted=[])
    ],
    max_wait_for_response=1)

AT_INITIAL_SETUP_SEQUENCE = [AT_WRITE_FULL_PHONE_FUNCTIONALITY,
                             AT_WRITE_OLD_SCRAMBLING_ALGORITHM,
                             AT_WRITE_TURN_OFF_PSM,
                             AT_WRITE_CONNECTION_STATUS_URC,
                             AT_WRITE_ENABLE_WAKEUP_INDICATION,

                             AT_WRITE_OPERATOR_SELECTION,
                             AT_EXECUTE_EXTENDED_SIGNAL_QUALITY,
                             AT_READ_OPERATOR_SELECTION,
                             AT_WRITE_ATTACH_TO_PACKET_DOMAIN_SERVICE]

AT_BASIC_INFO_SEQUENCE = [at_read_ati, at_read_imei, at_read_power_supply_voltage, at_read_operator_selection]
AT_OPEN_SOCKET_SEQUENCE = []
AT_SEND_UDP_MESSAGE_SEQUENCE = []

TEMP_AT_MAKE_CONNECTION = [

    at_read_pdp_context_status,
    at_write_pdp_context_status_deactivate,
    at_read_pdp_context_status,
    at_write_pdp_context_status_activate,
    at_read_pdp_context_status,

    at_write_activate_pdn_ctx

]
