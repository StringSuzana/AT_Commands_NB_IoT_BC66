#include "AtCommand.h"
/***
 * Takes pointer to atCommand and replaces <param> with given value.
 * Works only if param is longer than value. Cloud be modified to work even if value is bigger if needed.
 * **/
void at_command_replace_param_in_command(const AtCommand *at_command, const char *param, char *value)
{
    char new_command[MAX_COMMAND_LEN] = { 0 };
    strcpy(new_command, at_command->command);
    char* match = strstr(new_command, param);
    int match_index = match - new_command;

    if (match != NULL)
    {
        //printf("%s", match);

        if (strlen(param) >= (strlen(value) + 1)) // NULL TERMINATOR
        {
            const size_t param_len = strlen(param);
            const size_t value_len = strlen(value);
            const int rest_len = param_len - value_len;
            strncpy(match, value, param_len);
            for (int i = 1; i <= rest_len; i++)
            {
                new_command[match_index + i] = new_command[match_index + rest_len + i];
            }
            strncpy_s(at_command->command, strlen(at_command->command), new_command, strlen(at_command->command));
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
        AtResponse *responses = at_command->expected_responses->responses[i];
        for (int j = 0; j < responses->response_size; j++)
        {
            free(responses->responses[j]);
        }
        free(responses->wanted);
    }
    free(at_command->expected_responses->responses);
    free(at_command);
}*/
