#include "AtReader.h"
#include "string.h"
#include <stdio.h>
#include "StringArray.h"
#include "TimeUtils.h"

AtReader initAtReader()
{
    AtReader atReader = {
            .current_response = "",
            .at_response = NULL, // LIST OF STRINGS
            .at_status = STATUS_WAITING,
            .at_expected_response = NULL // AtResponse
    };
    return atReader;
}

String fromSerial(Serial *serial)
{
    String out = serial_read(serial);
    return out;
}
// function to check if a string starts with another string
bool startsWith(char *str, char *prefix)
{
    return strncmp(str, prefix, strlen(prefix)) == 0;
}

// function to split a string into an array of strings based on newline characters
int splitString(char *str, char **arr, int max_arr_size)
{
    int arr_size = 0;
    char *token = strtok(str, "\n");
    while (token != NULL && arr_size < max_arr_size)
    {
        arr[arr_size++] = token;
        token = strtok(NULL, "\n");
    }
    return arr_size;
}

// function to remove a string from an array of strings at a given index
void removeString(char **arr, int index, int arr_size)
{
    for (int i = index; i < arr_size - 1; i++)
    {
        arr[i] = arr[i + 1];
    }
    arr[arr_size - 1] = NULL;
}

// function to check if a response message contains the expected response
bool checkIfMessageIsWhole(AtReader *self, ResponseStatus for_status, char *expected_response, char **response_array,
                           int response_count)
{
    for (int i = 0; i < response_count; i++)
    {
        char *response = response_array[i];
        if (startsWith(response, expected_response))
        {
            self->at_status = for_status;
            removeString(response_array, i, response_count);
            return true;
        }
    }
    return false;
}

void remove_carriage_return(char *str)
{
    int i, j;
    for (i = 0, j = 0; str[i] != '\0'; i++)
    {
        if (str[i] != '\r')
        {
            str[j++] = str[i];
        }
    }
    str[j] = '\0';
}

void parseMessage(AtReader *self, AtCommand *at_command_obj, String string_from_serial)
{
    if (string_from_serial.length == 0)
    {
        return;
    }

    char *concatenated = malloc(strlen(self->current_response) + string_from_serial.length + 1);
    strcpy(concatenated, self->current_response);
    strncat(concatenated, string_from_serial.text, string_from_serial.length);
    self->current_response = malloc(strlen(concatenated));
    strcpy(self->current_response, concatenated);

    char **response_array = malloc(MAX_RESPONSE_LINES * sizeof(char *));
    int response_size = 0; //todo

    // split the response into an array of strings
    remove_carriage_return(self->current_response);
    char *line = strtok(self->current_response, "\n");
    while (line != NULL && response_size < MAX_RESPONSE_LINES)
    {
        if (strcmp(line, at_command_obj->command) != 0)//at_command_obj->command is ATI + 0000000...
        { // exclude the command that was sent
            response_array[response_size++] = line;
        }
        line = strtok(NULL, "\n");
    }

    if (response_size == 0)
    {
        free(response_array);
        return;
    }

    /* strncpy(self->current_response, line, MAX_RESPONSE_ROW_SIZE);
     self->current_response[MAX_RESPONSE_ROW_SIZE - 1] = '\0';

 */

    for (int i = 0; i < at_command_obj->expected_responses_size; i++)
    {
        AtResponse expected_response = at_command_obj->expected_responses.responses[i];
        if (checkIfMessageIsWhole(self, expected_response.status, expected_response.response, response_array,
                                  response_size))
        {
            AtResponse *at_response = AtResponse_create(expected_response.status, response_array, response_size,
                                                        expected_response.wanted, expected_response.wanted_size);
            self->at_expected_response = at_response;
            free(response_array);
            return;
        }
    }

    self->at_status = STATUS_WAITING;
    free(response_array);
    return;
}


AtResponse *answer(ResponseStatus result_status, char **result_array, int result_array_size, AtResponse *expected)
{
    if (result_status == STATUS_OK)
    {
        if (result_array_size == 0)
        {
            AtResponse *response = malloc(sizeof(AtResponse));
            response->status = result_status;
            response->response_size = result_array_size;
            response->wanted_size = 0;
            return response;
        } else
        {
            printf("AT STATUS: %d\nRESPONSE: ", result_status);
            for (int i = 0; i < result_array_size; i++)
            {
                printf("%s ", result_array[i]);
            }
            printf("\n");

            AtResponse *response = malloc(sizeof(AtResponse));
            response->status = result_status;
            response->response_size = result_array_size;
            response->wanted_size = 0;
            for (int i = 0; i < result_array_size; i++)
            {
                response->response[i] = result_array[i];
            }
            return response;
        }
    } else
    {
        AtResponse *response = malloc(sizeof(AtResponse));
        response->status = result_status;
        response->response_size = result_array_size;
        response->wanted_size = 0;
        return response;
    }
}

AtResponse *readAtResponse(AtReader *self, Serial *serial, AtCommand *at)
{
    String serial_msg = fromSerial(serial);
    int wait_intervals = at->max_wait_for_response;

    while (self->at_status == STATUS_WAITING && wait_intervals >= 0)
    {
        parseMessage(self, at, serial_msg);
        serial_msg = fromSerial(serial);
        wait_intervals--; // I want to sleep only 1 second at a time
        delay(1);
    }
    AtResponse *r = answer(self->at_status, self->at_response, sizeof(self->at_response),
                           self->at_expected_response);
    return r;
}

// AtResponse read_answer(Status result_status, const char **result_array, size_t result_array_len, AtResponse *at_expected_response)
// {
//     AtResponse response;
//     response.response_size = 0;
//     response.status = STATUS_ERROR;
//     response.wanted_size = 0;
//     return response;
// }
/*AtResponse *readAtResponse(AtReader *self, Serial *serial, AtCommand *at)
{
}*/


StringArray *getResponseRowFrom_Array(char *arr[], int row)
{
    char delim[] = ":";
    char str[MAX_RESPONSE_ROW_SIZE * MAX_RESPONSE_LINES];
    strcpy(str, arr[row]);

    char *str_token = strtok(str, delim);

    char **response_array = calloc(0, sizeof(char *));
    int i = 0;
    while (str_token != NULL)
    {
        response_array = realloc(response_array, i + 1 * sizeof(char *));
        response_array[i] = calloc(MAX_RESPONSE_ROW_SIZE, sizeof(char *));
        response_array[i] = strdup(str_token);
        str_token = strtok(NULL, delim);
        i++;
    }
    StringArray *stringArray = createStringArray(response_array, i);
    return stringArray;
}

AtResponse answerWithWantedParams(ResponseStatus result_status, char *result_array[], int result_array_len,
                                  const AtResponse *at_expected_response)
{
    if (result_array_len == 0)
    {
        printf("There is nothing to read");
        return (AtResponse) {.status = result_status, .response = result_array, .response_size = result_array_len, .wanted = NULL, .wanted_size = 0};
    } else if (at_expected_response->wanted_size == 0)
    {
        return (AtResponse) {.status = result_status, .response = result_array, .response_size = result_array_len, .wanted = NULL, .wanted_size = 0};
    } else
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
            StringArray *response_row = getResponseRowFrom_Array(result_array, row);
            StringArray *expected_row = getResponseRowFrom_Array(at_expected_response->response, row);

            int param_index = find_index(expected_row->arr, at_expected_response->wanted[i].name, expected_row->size);
            if (param_index != NOT_FOUND)
            {
                printf("Wanted param: %s ", response_row->arr[param_index]);

                wanted_params[i] = (Param) {
                        .name = at_expected_response->wanted[i].name,
                        .value = strdup(response_row->arr[param_index]),
                        .response_row = row};
            }
            destroyStringArray(response_row);
            destroyStringArray(expected_row);
        }

        return (AtResponse) {.status = result_status, .response = result_array, .response_size = result_array_len, .wanted = wanted_params, .wanted_size = at_expected_response->wanted_size};
    }
}