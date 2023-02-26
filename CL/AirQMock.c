#include "AirQMock.h"
#include <stdio.h>
#include "Serial.h"
#include "NbIoT.h"
#include "at_commands/AtCommands.c"
#include "AtReader.h"

AtSender sender = {
        .serverIpAddress = "IP_ADDR",
        .serverPort = "PORT",
        .protocol = "UDP",
        .wholeResponse = ""};

AtResponse AirQMock_sendMessageOverNbIoT(AirQMock *self, char *messageToSend, AtResponseCallback at_response_callback)
{
    // TODO: replace with more general methods than this direct two:
    AtCommand ati = at_read_ati();
    AtResponse response = executeAtCommand(&sender, self->serial, &ati);

    resetWholeResponse(&sender);
    at_response_callback(&response);
}
AtResponse AirQMock_initialSequence(AirQMock *self, AtResponseCallback at_response_callback)
{
    // TODO: replace with more general methods than this direct two:
    AtCommand ati = at_read_ati();
    AtResponse response = executeAtCommand(&sender, self->serial, &ati);

    resetWholeResponse(&sender);
    at_response_callback(&response);
}
void AirQMock_ProcessAtResponse(AtResponse *resulting_at_response)
{
    printf("\nTODO: In processing method");
    //printf("%s",*resulting_at_response->rows_array);
    // TODO
}

void test_answerWithWantedParams(AirQMock *self, AtResponseCallback at_response_callback)
{
    AtCommand cmd = at_read_imei();

    ResponseStatus result_status = STATUS_OK;
    //char *result_array[] = {"+CGSN:123456987", "OK"};
    AtResponse response = executeAtCommand(&sender, self->serial, &cmd);

//(ResponseStatus result_status, AtResponse response, const AtResponse *at_expected_response)

    at_response_callback(&response);
}