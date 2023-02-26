#include "NbIoT.h"
#include "AtReader.h"
#include "time_utils/TimeUtils.h"
#include <stdio.h>
#include <string.h>
#include "at_commands/AtCommands.c"
#include "at_commands/AtCommand.h"


void resetWholeResponse(AtSender *self)
{ self->wholeResponse, ""; }

char *getNbIotModuleInfo(AtSender *self)
{
    // char *rows = executeAtCommandSequence(AT_BASIC_INFO_SEQUENCE);
    char *response = "RESPONSE";
    return response;
}

AtResponse *executeAtCommand(AtSender *self, Serial *serial, AtCommand *at)
{
    char *cmd_and_description = "\n%s |>>| %s\n";
    printf(cmd_and_description, at->command, at->description);
    int command_len = strlen(at->command);
    serial_write(serial, at->command, command_len);
    delay(1);
    AtReader atReader = initAtReader();
    AtResponse *response = readAtResponse(&atReader, serial, at);
    return response;
}

AtResponse sendMessageToServer(AtSender *self, Serial *serial, char *message_text)
{
    resetWholeResponse(self);
    int message_length = strlen(message_text);
    char message_length_string[6];
    itoa(message_length, message_length_string, 10);

    AtCommand at_send_hex_command = at_read_imei(); //TODO: Replace with send_hex_message command
    at_command_replace_param_in_command(&at_send_hex_command, "<send_length>", message_length_string);
    at_command_replace_param_in_command(&at_send_hex_command, "<hex_string>", message_text);
    AtResponse *response = executeAtCommand(self, serial, &at_send_hex_command);

}