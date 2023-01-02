#include <stdlib.h>
#include "AtResponseArray.h"


AtResponseArray *create_at_responses_array(const int size, AtResponse at_responses[])
{
    AtResponseArray *array = malloc(sizeof(AtResponseArray));
    //array->responses_size = size;

    //array->responses = malloc(size * sizeof(AtResponse));
    //for (int i = 0; i < size; i++)
    //{
    //    // memcpy
    //    array->responses[i] = at_responses[i];
    //}
    return array;
}

void destroy_at_responses_array(AtResponseArray *array)
{
    for (int i = 0; i < array->responses_size; i++)
    {
        AtResponse *response = &array->responses[i];
        for (int j = 0; j < response->response_size; j++)
        {
            free(response->response[j]);
        }
        free(response->response);
        free(response->wanted);
    }
    free(array->responses);
}
