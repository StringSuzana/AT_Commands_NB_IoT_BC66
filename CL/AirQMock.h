#ifndef AIR_Q_MOCK_H
#define AIR_Q_MOCK_H

#include "AtResponseCallback.h"
#include "Serial.h"

typedef struct
{
    char *messageToSend;
    AtResponseCallback at_response_callback;
    Serial *serial;
} AirQMock;

AtResponse AirQMock_sendMessageOverNbIoT(AirQMock *self,char *messageToSend, AtResponseCallback at_response_callback);
void AirQMock_ProcessAtResponse(AtResponse *resulting_at_response);

#endif /* AIR_Q_MOCK_H */
