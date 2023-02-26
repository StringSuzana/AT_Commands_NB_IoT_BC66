#ifndef AT_COMMAND_H
#define AT_COMMAND_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../array_utils/AtResponseArray.h"


typedef struct
{
    char command[MAX_COMMAND_LEN];
    const char description[MAX_DESCRIPTION_LEN];
    int expected_responses_size;
    AtResponseArray expected_responses;
    int max_wait_for_response;
} AtCommand;

void at_command_replace_param_in_command(const AtCommand* at_command, const char* param, char* value);
//AtCommand *createAtCommand(const char *command, const char *description, int expected_responses_size, AtResponsesArray *expected_responses, int max_wait_for_response);
//void destroyAtCommand(AtCommand *at_command);

#endif
