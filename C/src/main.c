#include <stdio.h>
#include "Serial.h"
#include "AirQMock.h"

int main()
{
	printf("==PROGRAM STARTED==\n");
	AirQMock airQ = {
		.messageToSend = "Send this message",
		.at_response_callback = ProcessAtResponse};

	sendMessageOverNbIoT(airQ.messageToSend, airQ.at_response_callback);

	return (0);
}
