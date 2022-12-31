#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "AtCommand.h"

void AtCommand_replaceParamInCommand(AtCommand *at_command, char *param, char *value)
{
    char new_command[MAX_COMMAND_LEN];
    sprintf(new_command, at_command->command, param, value);
    strcpy(at_command->command, new_command);
}
