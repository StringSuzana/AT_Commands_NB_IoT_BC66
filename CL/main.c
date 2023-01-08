#include <stdio.h>
#include "Serial.h"
#include "AirQMock.h"
#include "AtCommand.h"
#include "AtCommands.c"
#include "AtReader.h"
void test_answerWithWantedParams();

int main()
{
    Serial *serial = serial_open("\\\\.\\COM19", CBR_9600, 301);
    printf("==PROGRAM STARTED==\n");
    AirQMock airQ = {
            .messageToSend = "Send this message",
            .at_response_callback = AirQMock_ProcessAtResponse,
            .serial = serial};

    AirQMock_sendMessageOverNbIoT(&airQ,airQ.messageToSend, airQ.at_response_callback);


    return (0);
}

void test_answerWithWantedParams()
{
    AtCommand cmd = at_read_imei();

    ResponseStatus result_status = STATUS_OK;
    char *result_array[] = {"+CGSN:123456987", "OK"};

    const AtResponse expected_response = {
            .status = STATUS_OK,
            .response_size = 4,
            .response = {"+CGSN:<IMEI>", "OK"},
            .wanted_size = 1,
            .wanted = {{.name = "<IMEI>", .value = "", .response_row = 0}}
    };
    answerWithWantedParams(result_status, result_array, 2, &expected_response);

}