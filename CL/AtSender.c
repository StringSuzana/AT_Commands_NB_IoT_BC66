#include <stdio.h>
#include "TimeUtils.h"
#include <string.h>
#include "AtSender.h"
#include "AtReader.h"

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
{
    self->wholeResponse, "";
}

char *getNbIotModuleInfo(AtSender *self)
{
    // char *response = executeAtCommandSequence(AT_BASIC_INFO_SEQUENCE);
    char *response = "RESPONSE";
    return response;
}

void executeAtCommand(AtSender *self, Serial *serial, AtCommand at)
{
    char *cmd_and_descr = "\n%s |>>| %s\n";
    printf(cmd_and_descr, at.command, at.description);
    int command_len = strlen(at.command);
    serial_write(serial, at.command, command_len);
    delay(1);
    AtReader atReader = initAtReader();
    readAtResponse(&atReader, serial, at);
    // serial_read(serial);
}
