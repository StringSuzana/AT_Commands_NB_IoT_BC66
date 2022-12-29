#ifndef AT_COMMAND_H
#define AT_COMMAND_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "AtResponseFunctionPointer.h"
#define MAX_DESCRIPTION_LEN 256
#define MAX_COMMAND_LEN 256
#define MAX_LONG_DESCRIPTION_LEN 1024

typedef struct
{
    char command[MAX_COMMAND_LEN];
    char description[MAX_DESCRIPTION_LEN];
    AtResponse **expected_responses;
    int expected_response_count;
    AtResponseFunctionPointer read_response_method; // TODO: Maybe delete, replace with only one function
    char long_description[MAX_LONG_DESCRIPTION_LEN];
    int max_wait_for_response;
} AtCommand;

AtCommand *AtCommand_create(char *command, char *description, AtResponse **expected_responses, int expected_response_count, AtResponseFunctionPointer read_response_method, char *long_description, int max_wait_for_response);
void AtCommand_replaceParamInCommand(AtCommand *at_command, char *param, char *value);
void AtCommand_destroy(AtCommand *at_command);

#endif
