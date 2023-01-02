#ifndef AT_RESPONSES_ARRAY_H
#define AT_RESPONSES_ARRAY_H
#include "AtResponse.h"
#define MAX_RESPONSES 5

typedef struct
{
    AtResponse responses[MAX_RESPONSES];
    int responses_size;
} AtResponseArray;

AtResponseArray *create_at_responses_array(int size, AtResponse at_responses[]);
void destroy_at_responses_array(AtResponseArray *array);

#endif /* AT_RESPONSES_ARRAY_H */
