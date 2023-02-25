#ifndef AT_RESPONSES_ARRAY_H
#define AT_RESPONSES_ARRAY_H
#include "../AtResponse.h"
#define MAX_RESPONSES 5

typedef struct
{
    AtResponse responses[MAX_RESPONSES];
    int responses_size;
} AtResponseArray;



#endif /* AT_RESPONSES_ARRAY_H */
