#include "AirQMock.h"
#include <stdio.h>
#include "Serial.h"
#include "NbIoT.h"
#include "at_commands/AtCommands.c"


AtSender sender = {
        .serverIpAddress = "IP_ADDR",
        .serverPort = "PORT",
        .protocol = "UDP",
        .wholeResponse = ""};

AtResponse AirQMock_sendMessageOverNbIoT(AirQMock *self, char *messageToSend, AtResponseCallback at_response_callback)
{
    // TODO: replace with more general methods than this direct two:
    AtCommand ati = at_read_ati();
    AtResponse* response = executeAtCommand(&sender, self->serial, &ati);

    resetWholeResponse(&sender);
    at_response_callback(&response);
}

AtResponse AirQMock_initialSequence(AirQMock *self, AtResponseCallback at_response_callback)
{
    // TODO: replace with more general methods than this direct two:
    AtCommand ati = at_read_ati();
    AtResponse *response = executeAtCommand(&sender, self->serial, &ati);

    resetWholeResponse(&sender);
    at_response_callback(&response);
}

void AirQMock_ProcessAtResponse(AtResponse *resulting_at_response)
{
    //TODO:
    printf("\nIn processing method\n");
    printf("AtResponse:\n");
    printf("status: %d\n", resulting_at_response->status);
    printf("rows_array:\n");
    for (int i = 0; i < resulting_at_response->rows_array.size; i++)
    {
        printf("  Row %d: ", i);
        for (int j = 0; j < MAX_STRING_ARRAY_ELEMENTS; j++)
        {
            if (resulting_at_response->rows_array.values[i].text[j] == '\0')
            {
                break;
            }
            printf("%c", resulting_at_response->rows_array.values[i].text[j]);
        }
        printf("\n");
    }
    printf("wanted_params_array:\n");
    for (int i = 0; i < resulting_at_response->wanted_params_size; i++)
    {
        printf("  Param %d:\n", i);
        printf("    name: %s\n", resulting_at_response->wanted_params_array[i].name);
        printf("    value: %s\n", resulting_at_response->wanted_params_array[i].value);
        printf("    response_row: %d\n", resulting_at_response->wanted_params_array[i].response_row);
    }
}

void test_answerWithWantedParams(AirQMock *self, AtResponseCallback at_response_callback)
{
    AtCommand cmd = at_read_imei();

    ResponseStatus result_status = STATUS_OK;
    //char *result_array[] = {"+CGSN:123456987", "OK"};
    AtResponse* response = executeAtCommand(&sender, self->serial, &cmd);

//(ResponseStatus result_status, AtResponse response, const AtResponse *at_expected_response)

    at_response_callback(response);
}