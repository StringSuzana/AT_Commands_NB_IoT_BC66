#include "AtReader.h"
#include "string.h"
#include <stdio.h>
#include "string_utils/CharPtrArray.h"
#include "TimeUtils.h"
#include "ResponseStatusNames.h"

void copyFromSerialToSelfCurrentResponse(AtReader *self, String string_from_serial);

void populateArrayWithTokensFromString(StringArray *string_array, char *string, AtCommand *at_command_obj);

void parseMessage(AtReader *self, AtCommand *at_command_obj, String string_from_serial);

AtReader initAtReader()
{
    AtReader atReader = {
            .current_response = "",
            .at_responses = NULL, // LIST OF STRINGS
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
// function to check if a values starts with another values
bool startsWith(char *str, char *prefix)
{
    return strncmp(str, prefix, strlen(prefix)) == 0;
}

bool starts_with(char *string, char *string_with_colon)
{
    char *colon_pos = strrchr(string_with_colon, ':');
    if (colon_pos == NULL)
    {
        // If ':' is not found in string string_with_colon, return false
        return false;
    }
    size_t len = colon_pos - string_with_colon;
    return strncmp(string, string_with_colon, len) == 0;
}

// function to split a values into an array of strings based on newline characters
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

// function to remove a values from an array of strings at a given index
void removeString(char **arr, int index, int arr_size)
{
    for (int i = index; i < arr_size - 1; i++)
    {
        arr[i] = arr[i + 1];
    }
    arr[arr_size - 1] = NULL;
}

// function to check if a responses message contains the expected responses
bool checkIfMessageIsWhole(AtReader *self, ResponseStatus for_status, char *expected_response_array[],
                           int expected_response_array_size,
                           StringArray response_array)
{
    int count_true = 0;
    for (int i = 0; i < expected_response_array_size; i++)
    {
        char *response = response_array.values[i].text;
        if (strcmp(response, expected_response_array[i]) == 0)
        {
            count_true += 1;
        }
        else if (starts_with(response, expected_response_array[i]))
        {
            count_true += 1;
        }
    }
    if (count_true == response_array.array_size)
    {
        self->at_status = for_status;
        return true;
    } else return false;
}


void populateArrayWithTokensFromString(StringArray *string_array, char *string, AtCommand *at_command_obj)
{
    int response_size = 0;
    // split the responses into an array of strings
    char *token_string = strdup(string);
    char *line = strtok(token_string, "\n");

    while (line != NULL && response_size < MAX_RESPONSE_LINES)
    {
        if (strcmp(line, at_command_obj->command) != 0)//at_command_obj->command is ATI + 0000000...
        { // exclude the command that was sent
            string_array->values[response_size].text = strdup(line);
            string_array->values[response_size++].length = strlen(line);
        }
        line = strtok(NULL, "\n");
    }
    string_array->array_size = response_size;
    free(token_string);
    free(line);
}

void copyFromSerialToSelfCurrentResponse(AtReader *self, String string_from_serial)
{
    char *concatenated = malloc(strlen(self->current_response) + string_from_serial.length + 1);
    strcpy(concatenated, self->current_response);
    strncat(concatenated, string_from_serial.text, string_from_serial.length);
    self->current_response = malloc(strlen(concatenated));

    strcpy(self->current_response, concatenated);
    free(concatenated);
}

void parseMessage(AtReader *self, AtCommand *at_command_obj, String string_from_serial)
{
    if (string_from_serial.length == 0)
    {
        return;
    }
    copyFromSerialToSelfCurrentResponse(self, string_from_serial);
    removeCarriageReturn(self->current_response);

    //char *response_array[MAX_RESPONSE_LINES] = {0};
    StringArray responseStringArray;
    populateArrayWithTokensFromString(&responseStringArray, self->current_response, at_command_obj);//todo: free

    for (int i = 0; i < at_command_obj->expected_responses_size; i++)
    {
        AtResponse expected_at = at_command_obj->expected_responses.responses[i];

        if (checkIfMessageIsWhole(self, expected_at.status, expected_at.responses, expected_at.response_size,
                                  responseStringArray))
        {
            //If message is whole, then we can also populate at_responses array
            populateArrayWithTokensFromString(&self->at_responses, self->current_response, at_command_obj);//todo: free


            AtResponse *at_expected_response = AtResponse_create(expected_at.status, expected_at.responses,
                                                                 expected_at.response_size, expected_at.wanted,
                                                                 expected_at.wanted_size);

            self->at_expected_response = at_expected_response; //todo: free
            return;
        }
    }

    self->at_status = STATUS_WAITING;

/*
    for (int i = 0; response_size >= 0; i--)
    {
        free(response_array[response_size]);
    }
*/

}


AtResponse *answer(ResponseStatus result_status, StringArray result_array, AtResponse *expected)
{
    if (result_status == STATUS_OK)
    {
        if (result_array.array_size == 0)
        {
            AtResponse *response = malloc(sizeof(AtResponse));
            response->status = result_status;
            response->response_size = result_array.array_size;
            response->wanted_size = 0;
            return response;
        } else
        {
            printf("AT STATUS: %s\nRESPONSE: ", getStatusName(result_status));
            for (int i = 0; i < result_array.array_size; i++)
            {
                printf("%s ", result_array.values[i].text);
            }
            printf("\n");

            AtResponse *response = malloc(sizeof(AtResponse));
            response->status = result_status;
            response->response_size = result_array.array_size;
            response->wanted_size = 0;
            for (int i = 0; i < result_array.array_size; i++)
            {
                response->responses[i] = result_array.values[i].text;
            }
            return response;
        }
    } else
    {
        AtResponse *response = malloc(sizeof(AtResponse));
        response->status = result_status;
        response->response_size = result_array.array_size;
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
        serial_msg = fromSerial(serial);//nothing is returned. TODO: fix
        wait_intervals--; // I want to sleep only 1 second at a time
        delay(1);
    }
    AtResponse *r = answer(self->at_status, self->at_responses, self->at_expected_response);
    return r;
}

// AtResponse read_answer(Status result_status, const char **result_array, size_t result_array_len, AtResponse *at_expected_response)
// {
//     AtResponse responses;
//     responses.response_size = 0;
//     responses.status = STATUS_ERROR;
//     responses.wanted_size = 0;
//     return responses;
// }
/*AtResponse *readAtResponse(AtReader *self, Serial *serial, AtCommand *at)
{
}*/


CharPtrArray *getResponseRowFrom_Array(char *arr[], int row)
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
    CharPtrArray *stringArray = createStringArray(response_array, i);
    return stringArray;
}

AtResponse answerWithWantedParams(ResponseStatus result_status, char *result_array[], int result_array_len,
                                  const AtResponse *at_expected_response)
{
    if (result_array_len == 0)
    {
        printf("There is nothing to read");
        return (AtResponse) {.status = result_status, .responses = result_array, .response_size = result_array_len, .wanted = NULL, .wanted_size = 0};
    } else if (at_expected_response->wanted_size == 0)
    {
        return (AtResponse) {.status = result_status, .responses = result_array, .response_size = result_array_len, .wanted = NULL, .wanted_size = 0};
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
            CharPtrArray *response_row = getResponseRowFrom_Array(result_array, row);
            CharPtrArray *expected_row = getResponseRowFrom_Array(at_expected_response->responses, row);

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

        return (AtResponse) {.status = result_status, .responses = result_array, .response_size = result_array_len, .wanted = wanted_params, .wanted_size = at_expected_response->wanted_size};
    }
}