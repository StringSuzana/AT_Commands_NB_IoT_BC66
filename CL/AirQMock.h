#ifndef AIR_Q_MOCK_H
#define AIR_Q_MOCK_H

#include "at_responses/AtresponseCallback.h"
#include "Serial.h"

typedef struct
{
    char *messageToSend;
    AtResponseCallback at_response_callback;
    Serial *serial;
} AirQMock;

AtResponse AirQMock_sendMessageOverNbIoT(AirQMock *self,char *messageToSend, AtResponseCallback at_response_callback);
void AirQMock_ProcessAtResponse(AtResponse *resulting_at_response);
AtResponse AirQMock_initialSequence(AirQMock *self, AtResponseCallback at_response_callback);
void test_answerWithWantedParams(AirQMock *self, AtResponseCallback at_response_callback);

#endif /* AIR_Q_MOCK_H */
