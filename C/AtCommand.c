#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "AtCommand.h"
#include "AtResponse.h"

typedef struct
{
    char command[MAX_COMMAND_LEN];
    char description[MAX_DESCRIPTION_LEN];
    AtResponse **expected_responses;
    int expected_response_count;
    void (*read_response_method)();
    char long_description[MAX_LONG_DESCRIPTION_LEN];
    int max_wait_for_response;
} AtCommand;

AtCommand *AtCommand_create(char *command, char *description, AtResponse *expected_responses[], int expected_response_count, void *read_response_method, char *long_description, int max_wait_for_response)
{
    AtCommand *at_command = malloc(sizeof(AtCommand));
    strcpy(at_command->command, command);
    strcpy(at_command->description, description);
    strcpy(at_command->long_description, long_description);

    at_command->expected_responses = expected_responses;
    at_command->expected_response_count = expected_response_count;

    at_command->read_response_method = read_response_method;
    at_command->max_wait_for_response = max_wait_for_response;
    return at_command;
}

void AtCommand_replaceParamInCommand(AtCommand *at_command, char *param, char *value)
{
    char new_command[MAX_COMMAND_LEN];
    sprintf(new_command, at_command->command, param, value);
    strcpy(at_command->command, new_command);
}

/* void AtCommand_destroy(AtCommand *at_command)
{
    free(at_command);
} */
void AtCommand_destroy(AtCommand *at_command)
{
    for (int i = 0; i < at_command->expected_response_count; i++)
    {
        free_at_response(at_command->expected_responses[i]);
    }
    free(at_command->expected_responses);
    free(at_command);
}