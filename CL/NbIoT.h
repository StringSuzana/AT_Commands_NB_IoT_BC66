#ifndef NBIOTSENDER_H
#define NBIOTSENDER_H

#include "at_responses/AtResponse.h"
#include "at_commands/AtCommand.h"
#include "Serial.h"

#define IP_ADDR "Server.IP_ADDR"
#define PORT "Server.PORT"
#define UDP "Server.UDP"

typedef struct
{
    char *serverIpAddress;
    char *serverPort;
    char *protocol;
    char *wholeResponse;
} AtSender;

void resetWholeResponse(AtSender *self);

char *getNbIotModuleInfo(AtSender *self);

AtResponse executeAtCommand(AtSender *self, Serial *serial, AtCommand *at);

char *executeAtCommandSequence(AtSender *self, AtCommand *sequence);

char *makeTextFromResponse(AtSender *self, AtCommand at_command, AtResponse at_response, int i);

#endif // NBIOTSENDER_H