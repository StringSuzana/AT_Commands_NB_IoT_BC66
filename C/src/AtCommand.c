#include "AtCommand.h"

void at_command_replace_param_in_command(const AtCommand *at_command, const char *param, char *value)
{
    char new_command[MAX_COMMAND_LEN] = {0};
    strcpy(new_command, at);
    char *match = strstr(new_command, param);
    int match_index = match - new_command;
    printf("%s", match);

    if (match != NULL)
    {
        printf("%s", match);

        if (strlen(param) >= (strlen(value) + 1)) // NULL TERMINATOR
        {
            int param_len = strlen(param);
            int value_len = strlen(value);
            int rest_len = param_len - value_len;
            strncpy(match, value, param_len);
            for (int i = 1; i <= rest_len; i++)
            {
                new_command[match_index + i] = new_command[match_index + rest_len + i];
            }
            strncpy_s(at, strlen(at), new_command, strlen(at));
            printf("\n%s\n", new_command);
            printf("\n%s\n", at);
            // todo: replace at command
        }
        else
        {
            printf("Value too big for replacement");
        }
    }
}

/*
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
}*/
