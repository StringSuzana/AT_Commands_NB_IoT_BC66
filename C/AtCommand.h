#ifndef AT_COMMAND_H
#define AT_COMMAND_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "AtResponsesArray.h"
#define MAX_DESCRIPTION_LEN 256
#define MAX_COMMAND_LEN 256
#define MAX_LONG_DESCRIPTION_LEN 1024

typedef struct
{
    const char *command;
    const char *description;
    const char *long_description;
    int expected_responses_count;
    const AtResponsesArray expected_responses;
    int max_wait_for_response;
} AtCommand;
void AtCommand_replaceParamInCommand(AtCommand *at_command, char *param, char *value);

#endif
