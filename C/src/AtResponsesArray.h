#ifndef AT_RESPONSES_ARRAY_H
#define AT_RESPONSES_ARRAY_H
#include "AtResponse.h"
#define MAX_RESPONSES 5

typedef struct
{
    AtResponse responses[MAX_RESPONSES];
    int responses_size;
} AtResponsesArray;

AtResponsesArray *create_at_responses_array(int size, AtResponse atResponses[]);
void destroy_at_responses_array(AtResponsesArray *array);

#endif /* AT_RESPONSES_ARRAY_H */
