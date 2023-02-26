#ifndef AT_RESPONSE_H
#define AT_RESPONSE_H

#include <stdio.h>
#include "ResponseStatusEnum.h"
#include "Param.h"
#include "../string_utils/StringArray.h"

#define MAX_RESPONSE_LINES 10
#define MAX_RESPONSE_ROW_SIZE 1024
#define MAX_WANTED_PARAMS 10

typedef struct
{
    ResponseStatus status;
    StringArray rows_array;
    Param wanted_params_array[MAX_WANTED_PARAMS];
    int wanted_params_size;
} AtResponse;
AtResponse* AtResponse_create(ResponseStatus status, StringArray response, Param* wanted, int wanted_size);
void AtResponse_free ();

#endif /* AT_RESPONSE_H */
