#include <stdio.h>
#include "TimeUtils.h"
#include <string.h>
#include "NbIoTSender.h"

void resetWholeResponse(NbIoTSender *self)
{
    self->wholeResponse, "";
}

char *getNbIotModuleInfo(NbIoTSender *sender)
{
    // char *response = executeAtCommandSequence(AT_BASIC_INFO_SEQUENCE);
    char *response = "RESPONSE";
    return response;
}

void executeAtCommand(NbIoTSender *self, Serial *serial, AtCommand at)
{
    char *cmd_and_descr = "\n%s |>>| %s\n";
    printf(cmd_and_descr, at.command, at.description);
    int command_len = strlen(at.command);
    serial_write(serial, at.command, command_len);
    delay(1);
    serial_read(serial);
}
