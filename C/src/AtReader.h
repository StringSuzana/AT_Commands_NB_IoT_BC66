#ifndef AT_RESPONSE_READER_H
#define AT_RESPONSE_READER_H
#include <string.h>
#include <stdlib.h>

#include "AtCommand.h"
#include "AtResponse.h"
#include "ArrayUtils.h"
#include "Serial.h"

#define WAITING 0
#define NOT_FOUND -1

typedef struct
{
    char *current_response;
    char **at_response;
    int at_status;
    AtResponse *at_expected_response;
} AtReader;
AtResponse readAtResponse(AtReader *self, Serial *serial, AtCommand at);
AtResponse answerWithWantedParams(Status result_status, char *result_array[], int result_array_len, const AtResponse at_expected_response);

#endif /* AT_RESPONSE_READER_H */
