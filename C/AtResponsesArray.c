#include "AtResponsesArray.h"
AtResponsesArray create_at_response_array(SocketStatus status, char **response, int response_size,
                                          Param *wanted, int wanted_size)
{
    AtResponse **responses = malloc(response_size * sizeof(AtResponse *));
    for (int i = 0; i < response_size; i++)
    {
        responses[i] = malloc(sizeof(AtResponse));
        responses[i]->status = status;
        responses[i]->response = response[i];
        responses[i]->wanted = malloc(wanted_size * sizeof(Param));
        for (int j = 0; j < wanted_size; j++)
        {
            responses[i]->wanted[j] = wanted[j];
        }
        responses[i]->wanted_size = wanted_size;
    }
    AtResponsesArray array = {responses, response_size};
    return array;
}
