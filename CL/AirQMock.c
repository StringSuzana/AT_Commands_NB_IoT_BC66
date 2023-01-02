#include "AirQMock.h"
#include <stdio.h>
#include "Serial.h"
#include "NbIoT.h"
#include "AtCommands.c"

AtSender sender = {
    .serverIpAddress = "IP_ADDR",
    .serverPort = "PORT",
    .protocol = "UDP",
    .wholeResponse = ""};

AtResponse sendMessageOverNbIoT(char *messageToSend, AtResponseCallback at_response_callback)
{
    Serial *serial = serial_open("\\\\.\\COM19", CBR_9600, 301);
    // TODO: replace with more general methods than this direct two:
    executeAtCommand(&sender, serial, at_read_ati());
    resetWholeResponse(&sender);
}

void ProcessAtResponse(AtResponse *resulting_at_response)
{
    printf("In processing method");
    // TODO
}