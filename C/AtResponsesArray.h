#ifndef FFC7B860_A555_4902_9A77_66142B5A36C1
#define FFC7B860_A555_4902_9A77_66142B5A36C1
#include "AtResponse.h"
#define MAX_RESPONSES 5

typedef struct
{
    AtResponse responses[MAX_RESPONSES];
    int responses_size;
} AtResponsesArray;
#endif /* FFC7B860_A555_4902_9A77_66142B5A36C1 */
