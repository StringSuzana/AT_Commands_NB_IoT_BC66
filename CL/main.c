#include <stdio.h>
#include "Serial.h"
#include "AirQMock.h"
#include "at_commands/AtCommand.h"
#include "at_commands/AtCommands.c"
#include "AtReader.h"

int main()
{
    Serial *serial = serial_open("\\\\.\\COM19", CBR_9600, 301);
    printf("==PROGRAM STARTED==\n");
    AirQMock airQ = {
            .messageToSend = "Send this message",
            .at_response_callback = AirQMock_ProcessAtResponse,
            .serial = serial};

    //AirQMock_sendMessageOverNbIoT(&airQ,airQ.messageToSend, airQ.at_response_callback);

    test_answerWithWantedParams(&airQ,  airQ.at_response_callback);
    return (0);
}
