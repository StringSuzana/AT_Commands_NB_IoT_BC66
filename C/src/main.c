#include <stdio.h>
#include "Serial.h"
#include "NbIoTSender.h"
#include "AtCommands.c"

NbIoTSender sender = {
	.serverIpAddress = IP_ADDR,
	.serverPort = PORT,
	.protocol = UDP,
	.wholeResponse = ""};

int main()
{
	printf("Hello World!\n");
	Serial *serial = serial_open("\\\\.\\COM19", CBR_9600, 301);

	executeAtCommand(&sender, serial, at_read_ati());

	resetWholeResponse(&sender);

	return (0);
}
