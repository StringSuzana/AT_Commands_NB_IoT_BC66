#include "AtReader.h"

// AtResponse readAtResponse(Reader *self, Serial *serial, AtCommand *at_command_obj)
// {
//     char *serial_msg = fromSerial(serial);
//     int wait_intervals = at_command_obj->max_wait_for_response;

//     while (self->at_status == WAITING && wait_intervals >= 0)
//     {
//         parseMessage(self, at_command_obj, serial_msg);
//         serial_msg = fromSerial(serial);
//         wait_intervals--; // I want to sleep only 1 second at a time
//         sleep(1);
//     }
//     AtResponse r = read_answer(self->at_status, self->at_response, sizeof(self->at_response), self->at_expected_response);
//     return r;
// }
// AtResponse read_answer(Status result_status, const char **result_array, size_t result_array_len, AtResponse *at_expected_response)
// {
//     AtResponse response;
//     response.response_size = 0;
//     response.status = STATUS_ERROR;
//     response.wanted_size = 0;
//     return response;
// }
AtResponse readAtResponse(AtReader *self, Serial *serial, AtCommand *at)
{
}
char *fromSerial(Serial *serial)
{
    char *out = serial_read(serial);
    return out;
}
char **getResponseRowFrom_Array(char **arr, int row)
{
    char *response_row = strtok(arr[row], ":");
    char **response_array = malloc(MAX_WANTED_PARAMS * sizeof(char *));
    int i = 0;
    while (response_row != NULL)
    {
        response_array[i] = response_row;
        response_row = strtok(NULL, ",");
        i++;
    }
    return response_array;
}
AtResponse answerWithWantedParams(ResponseStatus result_status, char *result_array[], int result_array_len, const AtResponse *at_expected_response)
{
    if (result_array_len == 0)
    {
        printf("There is nothing to read");
        return (AtResponse){.status = result_status, .response = result_array, .response_size = result_array_len, .wanted = NULL, .wanted_size = 0};
    }
    else if (at_expected_response.wanted_size == 0)
    {
        return (AtResponse){.status = result_status, .response = result_array, .response_size = result_array_len, .wanted = NULL, .wanted_size = 0};
    }
    else
    {
        printf("AT STATUS: %d\nRESPONSE: ", result_status);
        for (int i = 0; i < result_array_len; i++)
        {
            printf("%s ", result_array[i]);
        }
        printf("\n");

        Param wanted_params[MAX_WANTED_PARAMS];

        for (int i = 0; i < at_expected_response->wanted_size; i++)
        {
            int row = at_expected_response->wanted[i].response_row;
            char *response_row = result_array[row];
            char *expected_row = at_expected_response->response[row];

            int param_index = find_index(expected_row, at_expected_response->wanted[i].name, strlen(expected_row));
            if (param_index != NOT_FOUND)
            {
                wanted_params[i] = (Param){.name = at_expected_response->wanted[i].name, .value = response_row[param_index], .response_row = row};
            }
        }

        return (AtResponse){.status = result_status, .response = result_array, .response_size = result_array_len, .wanted = wanted_params, .wanted_size = at_expected_response.wanted_size};
    }
}