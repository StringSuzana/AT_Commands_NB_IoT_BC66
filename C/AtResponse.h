#ifndef AT_RESPONSE_H
#define AT_RESPONSE_H
#include "SocketStatusEnum.h"
#include "Param.h"

typedef struct
{
    SocketStatus status;
    char **response;
    int response_size;
    Param *wanted;
    int wanted_size;
} AtResponse;

AtResponse *create_at_response(SocketStatus status, char **response, int response_size, Param *wanted, int wanted_size);
void free_at_response(AtResponse *at_response);

#endif /* AT_RESPONSE_H */
