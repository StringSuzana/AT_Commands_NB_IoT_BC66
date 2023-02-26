#include <malloc.h>
#include <string.h>
#include "AtResponse.h"

AtResponse* AtResponse_create(ResponseStatus status, char** response, int response_size, Param* wanted, int wanted_size) {
    AtResponse* at_response = malloc(sizeof(AtResponse));
    at_response->status = status;
    at_response->row_size = response_size;
    at_response->wanted_size = wanted_size;

    // Allocate memory for the rows strings
    for (int i = 0; i < response_size; i++) {
        at_response->rows[i] = malloc(MAX_RESPONSE_ROW_SIZE * sizeof(char));
        strcpy(at_response->rows[i], response[i]);
    }

    // Allocate memory for the wanted_params params
    for (int i = 0; i < wanted_size; i++) {
        at_response->wanted_params[i].name = malloc(MAX_RESPONSE_ROW_SIZE * sizeof(char));
        strcpy(at_response->wanted_params[i].name, wanted[i].name);
        at_response->wanted_params[i].value = malloc(MAX_RESPONSE_ROW_SIZE * sizeof(char));
        strcpy(at_response->wanted_params[i].value, wanted[i].value);
        at_response->wanted_params[i].response_row = wanted[i].response_row;
    }

    return at_response;
}

