#include <malloc.h>
#include <string.h>
#include "AtResponse.h"

AtResponse* AtResponse_create(ResponseStatus status, char** response, int response_size, Param* wanted, int wanted_size) {
    AtResponse* at_response = malloc(sizeof(AtResponse));
    at_response->status = status;
    at_response->response_size = response_size;
    at_response->wanted_size = wanted_size;

    // Allocate memory for the responses strings
    for (int i = 0; i < response_size; i++) {
        at_response->responses[i] = malloc(MAX_RESPONSE_ROW_SIZE * sizeof(char));
        strcpy(at_response->responses[i], response[i]);
    }

    // Allocate memory for the wanted params
    for (int i = 0; i < wanted_size; i++) {
        at_response->wanted[i].name = malloc(MAX_RESPONSE_ROW_SIZE * sizeof(char));
        strcpy(at_response->wanted[i].name, wanted[i].name);
        at_response->wanted[i].value = malloc(MAX_RESPONSE_ROW_SIZE * sizeof(char));
        strcpy(at_response->wanted[i].value, wanted[i].value);
        at_response->wanted[i].response_row = wanted[i].response_row;
    }

    return at_response;
}

