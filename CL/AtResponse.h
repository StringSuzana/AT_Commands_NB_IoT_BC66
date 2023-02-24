#ifndef AT_RESPONSE_H
#define AT_RESPONSE_H

#include <stdio.h>
#include "ResponseStatusEnum.h"
#include "Param.h"

#define MAX_RESPONSE_LINES 10
#define MAX_RESPONSE_ROW_SIZE 1024
#define MAX_WANTED_PARAMS 10

typedef struct
{
    ResponseStatus status;
    char *response[MAX_RESPONSE_LINES];
    int response_size;
    Param wanted[MAX_WANTED_PARAMS];
    int wanted_size;
} AtResponse;
AtResponse* AtResponse_create ();
void AtResponse_free ();

#endif /* AT_RESPONSE_H */
