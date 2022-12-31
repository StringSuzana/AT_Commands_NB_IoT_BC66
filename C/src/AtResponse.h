#ifndef AT_RESPONSE_H
#define AT_RESPONSE_H

#include <stdio.h>
#include "ResponseStatusEnum.h"
#include "Param.h"
#include "Param.h"

#define MAX_RESPONSE_LINES 10
#define MAX_WANTED_PARAMS 10

typedef struct
{
    Status status;
    char *response[MAX_RESPONSE_LINES];
    int response_size;
    Param wanted[MAX_WANTED_PARAMS];
    int wanted_size;
} AtResponse;
#endif /* AT_RESPONSE_H */
