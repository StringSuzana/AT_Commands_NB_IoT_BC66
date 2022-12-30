#ifndef NBIOTSENDER_H
#define NBIOTSENDER_H
#include "AtResponse.h"
#include "AtCommand.h"
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
} NbIoTSender;

void resetWholeResponse(NbIoTSender *sender);
char *getNbIotModuleInfo(NbIoTSender *sender);
void executeAtCommand(NbIoTSender *self, Serial *serial, AtCommand at);
char *executeAtCommandSequence(NbIoTSender *sender, AtCommand *sequence);
char *makeTextFromResponse(NbIoTSender *sender, AtCommand at_command, AtResponse at_response, int i);
#endif // NBIOTSENDER_H