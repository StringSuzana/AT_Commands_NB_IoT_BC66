#include <stdio.h>
//#include "Serial.h"
//#include "AirQMock.h"
#include "AtCommand.h"
#include "AtCommands.c"

int main()
{
    printf("==PROGRAM STARTED==\n");
    /* AirQMock airQ = {
             .messageToSend = "Send this message",
             .at_response_callback = ProcessAtResponse};

     sendMessageOverNbIoT(airQ.messageToSend, airQ.at_response_callback);*/

    AtCommand cmd = at_read_imei_replace_test();
    printf("Command before: %s", cmd.command);

    at_command_replace_param_in_command(&cmd, "<IMEI_PICK>", "1");
    printf("Command after: %s", cmd.command);
    return (0);
}
