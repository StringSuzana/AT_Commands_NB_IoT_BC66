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
AtCommand *createAtCommand(const char *command, const char *description, int expected_responses_size, AtResponsesArray *expected_responses, int max_wait_for_response)
{
    AtCommand *at_command = malloc(sizeof(AtCommand));
    at_command->command = malloc(strlen(command) + 1);

    strcpy(at_command->command, command);
    at_command->description = malloc(strlen(description) + 1);
    strcpy(at_command->description, description);

    at_command->expected_responses_size = expected_responses_size;
    at_command->expected_responses = expected_responses;
    at_command->max_wait_for_response = max_wait_for_response;

    return at_command;
}

void destroyAtCommand(AtCommand *at_command)
{
    free(at_command->command);
    free(at_command->description);
    for (int i = 0; i < at_command->expected_responses_size; i++)
    {
        AtResponse *response = at_command->expected_responses->responses[i];
        for (int j = 0; j < response->response_size; j++)
        {
            free(response->response[j]);
        }
        free(response->wanted);
    }
    free(at_command->expected_responses->responses);
    free(at_command);
}