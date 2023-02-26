#include "AtReader.h"
#include "time_utils/TimeUtils.h"
#include "at_responses/ResponseStatusNames.h"

void copyFromSerialToSelfCurrentResponse(AtReader *self, String string_from_serial);

void populateArrayWithTokensFromString(StringArray *string_array, char *string, AtCommand *at_command_obj);

void parseMessage(AtReader *self, AtCommand *at_command_obj, String string_from_serial);

AtReader initAtReader()
{
    AtReader atReader = {
            .current_response = "",
            .at_response_rows = NULL, // LIST OF STRINGS
            .at_status = STATUS_WAITING,
            .at_expected_response = NULL, // AtResponse
    };
    return atReader;
}

String fromSerial(Serial *serial)
{
    String out = serial_read(serial);
    return out;
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


// function to check if a rows_array message contains the expected rows_array
bool checkIfMessageIsWhole(AtReader *self, ResponseStatus for_status, StringArray expected_response_array, StringArray response_array)
{
    int count_true = 0;
    for (int i = 0; i < expected_response_array.size; i++)
    {
        char *response = response_array.values[i].text;
        char *expected_response = expected_response_array.values[i].text;

        if (strcmp(response, expected_response) == 0)
        {
            count_true += 1;
        } else if (starts_with(response, expected_response))
        {
            count_true += 1;
        }
    }
    if (count_true == response_array.size)
    {
        self->at_status = for_status;
        return true;
    } else return false;
}


void populateArrayWithTokensFromString(StringArray *string_array, char *string, AtCommand *at_command_obj)
{
    int response_size = 0;
    // split the rows_array into an array of strings
    char *token_string = strdup(string);
    char *line = strtok(token_string, "\n");

    while (line != NULL && response_size < MAX_RESPONSE_ROWS)
    {
        if (strcmp(line, at_command_obj->command) != 0)//at_command_obj->command is ATI + 0000000...
        { // exclude the command that was sent
            string_array->values[response_size].text = strdup(line);
            string_array->values[response_size++].length = strlen(line);
        }
        line = strtok(NULL, "\n");
    }
    string_array->size = response_size;
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

    //char *response_array[MAX_RESPONSE_ROWS] = {0};
    StringArray responseStringArray;
    populateArrayWithTokensFromString(&responseStringArray, self->current_response, at_command_obj);//todo: free

    for (int i = 0; i < at_command_obj->expected_responses_size; i++)
    {
        AtResponse expected_at = at_command_obj->expected_responses.responses[i];

        if (checkIfMessageIsWhole(self, expected_at.status, expected_at.rows_array,
                                  responseStringArray))
        {
            //If message is whole, then we can also populate at_response_rows array
            populateArrayWithTokensFromString(&self->at_response_rows, self->current_response, at_command_obj);//todo: free


            AtResponse *at_expected_response = AtResponse_create(expected_at.status,
                                                                 expected_at.rows_array,
                                                                 expected_at.wanted_params_array,
                                                                 expected_at.wanted_params_size);

            self->at_expected_response = at_expected_response; //todo: free
            return;
        }
    }

    self->at_status = STATUS_WAITING;

}


AtResponse *answer(ResponseStatus result_status, StringArray result_array, AtResponse *expected)
{
    if (result_status == STATUS_OK)
    {
        if (result_array.size == 0)
        {
            AtResponse *response = malloc(sizeof(AtResponse));
            response->status = result_status;
            response->rows_array.size = result_array.size;
            response->wanted_params_size = 0;
            return response;
        } else
        {
            printf("AT STATUS: %s\nRESPONSE: ", getStatusName(result_status));
            for (int i = 0; i < result_array.size; i++)
            {
                printf("%s ", result_array.values[i].text);
            }
            printf("\n");

            AtResponse *response = malloc(sizeof(AtResponse));
            response->status = result_status;
            response->rows_array.size = result_array.size;
            response->wanted_params_size = 0;
            for (int i = 0; i < result_array.size; i++)
            {
                response->rows_array.values[i].text = result_array.values[i].text;
            }
            return response;
        }
    } else
    {
        AtResponse *response = malloc(sizeof(AtResponse));
        response->status = result_status;
        response->rows_array.size = result_array.size;
        response->wanted_params_size = 0;
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
    //(ResponseStatus result_status, char *result_array[], int result_array_len, const AtResponse *at_expected_response);
    AtResponse *r = answerWithWantedParams(self->at_status, self->at_response_rows, self->at_expected_response);
    return r;
}

AtResponse *answerWithWantedParams(ResponseStatus result_status, StringArray string_rows, const AtResponse *at_expected_response)
{

    if (string_rows.size == 0)
    {
        printf("\nThere is no responses message\n");
        AtResponse *at_response_result = AtResponse_create(result_status, string_rows, NULL, 0);
        return at_response_result;
    } else if (at_expected_response->wanted_params_size == 0)
    {
        printf("\nThere is no wanted params\n");
        AtResponse *at_response_result = AtResponse_create(result_status, string_rows, NULL, 0);
        return at_response_result;
    } else
    {
        printf("AT STATUS: %s\nRESPONSE: ", getStatusName(result_status));
        for (int i = 0; i < string_rows.size; i++)
        {
            printf("%s ", string_rows.values[i].text);
        }
        printf("\n");

        Param *param_array = calloc(at_expected_response->wanted_params_size, sizeof(Param));

        for (int i = 0; i < at_expected_response->wanted_params_size; i++)
        {
            int row = at_expected_response->wanted_params_array[i].response_row;
            StringArray response_row = getResponseRowFrom_stringArray(string_rows, row);
            StringArray expected_row = getResponseRowFrom_stringArray(at_expected_response->rows_array, row);

            int param_index = findIndexIn_StringArray(expected_row, at_expected_response->wanted_params_array[i].name);
            if (param_index != NOT_FOUND)
            {
                param_array[i].name = strdup(expected_row.values[param_index].text);
                param_array[i].value = strdup(response_row.values[param_index].text);
                param_array[i].response_row = row;
            }
            printf("Wanted param_array: %s value: %s", param_array->name, response_row.values[param_index].text);


        }
        AtResponse *at_response_result = AtResponse_create(result_status, string_rows, param_array, at_expected_response->wanted_params_size);

        return at_response_result;
    }
}