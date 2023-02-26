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
    char *rows[MAX_RESPONSE_LINES];
    int row_size;
    Param wanted_params[MAX_WANTED_PARAMS];
    int wanted_size;
} AtResponse;
AtResponse* AtResponse_create(ResponseStatus status, char** response, int response_size, Param* wanted, int wanted_size);
void AtResponse_free ();

#endif /* AT_RESPONSE_H */
