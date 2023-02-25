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

AtResponse AirQMock_sendMessageOverNbIoT(AirQMock *self, char *messageToSend, AtResponseCallback at_response_callback)
{
    // TODO: replace with more general methods than this direct two:
    AtCommand ati = at_read_ati();
    AtResponse *response = executeAtCommand(&sender, self->serial, &ati);
    resetWholeResponse(&sender);
    at_response_callback(response);
}

void AirQMock_ProcessAtResponse(AtResponse *resulting_at_response)
{
    printf("TODO: In processing method");
    printf("%s",*resulting_at_response->responses);
    // TODO
}