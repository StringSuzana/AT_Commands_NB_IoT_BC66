#ifndef AT_RESPONSES_ARRAY_H
#define AT_RESPONSES_ARRAY_H
#include "../at_responses/AtResponse.h"

typedef struct
{
    AtResponse responses[MAX_RESPONSES];
    int responses_size;
} AtResponseArray;



#endif /* AT_RESPONSES_ARRAY_H */
