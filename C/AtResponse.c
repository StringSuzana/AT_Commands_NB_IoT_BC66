#include "AtResponse.h"

AtResponse *create_at_response(SocketStatus status, char **response, int response_size, Param *wanted, int wanted_size)
{
    AtResponse *at_response = malloc(sizeof(AtResponse));
    at_response->status = status;
    at_response->response = malloc(sizeof(char *) * response_size);
    for (int i = 0; i < response_size; i++)
    {
        at_response->response[i] = malloc(sizeof(char) * strlen(response[i]) + 1);
        strcpy(at_response->response[i], response[i]);
    }
    at_response->response_size = response_size;

    at_response->wanted = malloc(sizeof(Param) * wanted_size);
    for (int i = 0; i < wanted_size; i++)
    {
        at_response->wanted[i].name = malloc(sizeof(char) * strlen(wanted[i].name) + 1);
        strcpy(at_response->wanted[i].name, wanted[i].name);
        at_response->wanted[i].value = malloc(sizeof(char) * strlen(wanted[i].value) + 1);
        strcpy(at_response->wanted[i].value, wanted[i].value);
        at_response->wanted[i].response_row = wanted[i].response_row;
    }
    at_response->wanted_size = wanted_size;

    return at_response;
}

void free_at_response(AtResponse *at_response)
{
    for (int i = 0; i < at_response->response_size; i++)
    {
        free(at_response->response[i]);
    }
    free(at_response->response);

    for (int i = 0; i < at_response->wanted_size; i++)
    {
        free(at_response->wanted[i].name);
        free(at_response->wanted[i].value);
    }
    free(at_response->wanted);
    free(at_response);
}
