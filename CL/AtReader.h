#ifndef AT_RESPONSE_READER_H
#define AT_RESPONSE_READER_H

#include <string.h>
#include <stdlib.h>

#include "at_commands/AtCommand.h"
#include "at_responses/AtResponse.h"
#include "array_utils/ArrayUtils.h"
#include "Serial.h"
#include "string_utils/StringArray.h"



typedef struct
{
    char *current_response;
    StringArray at_response_rows;
    int at_status;
    AtResponse *at_expected_response;
} AtReader;

AtResponse *readAtResponse(AtReader *self, Serial *serial, AtCommand *at);

AtResponse* answerWithWantedParams(ResponseStatus result_status, StringArray response, const AtResponse *at_expected_response);

AtReader initAtReader();

#endif /* AT_RESPONSE_READER_H */
