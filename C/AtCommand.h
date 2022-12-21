#ifndef AT_COMMAND_H
#define AT_COMMAND_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DESCRIPTION_LEN 256
#define MAX_COMMAND_LEN 256
#define MAX_LONG_DESCRIPTION_LEN 1024

typedef struct AtCommand AtCommand;

AtCommand *AtCommand_create(char *command, char *description, AtResponse **expected_responses, int expected_response_count, void *read_response_method, char *long_description, int max_wait_for_response);
void AtCommand_replaceParamInCommand(AtCommand *at_command, char *param, char *value);
void AtCommand_destroy(AtCommand *at_command);

#endif
