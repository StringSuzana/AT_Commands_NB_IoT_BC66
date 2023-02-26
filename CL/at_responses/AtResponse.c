#include <malloc.h>
#include <string.h>
#include "AtResponse.h"

AtResponse* AtResponse_create(ResponseStatus status, StringArray response, Param* wanted, int wanted_size) {
    AtResponse* at_response = malloc(sizeof(AtResponse));

    at_response->status = status;
    memcpy(&at_response->rows_array, &response, sizeof(StringArray));

    at_response->wanted_params_size = wanted_size;

    // Allocate memory for the rows_array strings
    for (int i = 0; i < response.size; i++) {
        at_response->rows_array.values[i].text = calloc(MAX_RESPONSE_ROW_LENGTH, sizeof(char));
        at_response->rows_array.values[i].length = response.values[i].length;//or MAX_RESPONSE_ROW_LENGTH
        strcpy(at_response->rows_array.values[i].text, response.values[i].text);
    }

    // Allocate memory for the wanted_params_array params
    for (int i = 0; i < wanted_size; i++) {
        at_response->wanted_params_array[i].name = malloc(MAX_RESPONSE_ROW_LENGTH * sizeof(char));
        strcpy(at_response->wanted_params_array[i].name, wanted[i].name);
        at_response->wanted_params_array[i].value = malloc(MAX_RESPONSE_ROW_LENGTH * sizeof(char));
        strcpy(at_response->wanted_params_array[i].value, wanted[i].value);
        at_response->wanted_params_array[i].response_row = wanted[i].response_row;
    }

    return at_response;
}

