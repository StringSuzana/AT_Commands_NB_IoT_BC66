#include "NbIoT.h"
#include "AtReader.h"
#include "TimeUtils.h"
#include <stdio.h>
#include <string.h>
#include "AtCommands.c"
#include "AtCommand.h"

AtReader initAtReader()
{
    AtReader atReader = {
            .current_response = "",
            .at_response = NULL, // LIST OF STRINGS
            .at_status = STATUS_WAITING,
            .at_expected_response = NULL // AtResponse
    };
    return atReader;
}

void resetWholeResponse(AtSender *self)
{ self->wholeResponse, ""; }

char *getNbIotModuleInfo(AtSender *self)
{
    // char *response = executeAtCommandSequence(AT_BASIC_INFO_SEQUENCE);
    char *response = "RESPONSE";
    return response;
}

AtResponse *executeAtCommand(AtSender *self, Serial *serial, AtCommand *at)
{
    char *cmd_and_descr = "\n%s |>>| %s\n";
    printf(cmd_and_descr, at->command, at->description);
    int command_len = strlen(at->command);
    serial_write(serial, at->command, command_len);
    delay(1);
    AtReader atReader = initAtReader();
    AtResponse response = readAtResponse(&atReader, serial, at);
    return &response;
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