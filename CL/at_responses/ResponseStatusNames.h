#ifndef RESPONSE_STATUS_NAMES_H
#define RESPONSE_STATUS_NAMES_H

#include "ResponseStatusEnum.h"

const char* getStatusName(ResponseStatus status)
{
    switch (status)
    {
        case STATUS_ERROR:
            return "ERROR";
        case STATUS_OK:
            return "OK";
        case STATUS_WAITING:
            return "WAITING";
        default:
            return "";
    }
}
#endif //RESPONSE_STATUS_NAMES_H
