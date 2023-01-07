#include <stdio.h>
//#include "Serial.h"
//#include "AirQMock.h"
#include "AtCommand.h"
#include "AtReader.h"
#include "AtCommands.c"

int main()
{
    printf("==PROGRAM STARTED==\n");
    /* AirQMock airQ = {
             .messageToSend = "Send this message",
             .at_response_callback = ProcessAtResponse};

     sendMessageOverNbIoT(airQ.messageToSend, airQ.at_response_callback);*/

    AtCommand cmd = at_read_imei();
    //ResponseStatus result_status, char *result_array[], int result_array_len, const AtResponse *at_expected_response
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

    return (0);
}
