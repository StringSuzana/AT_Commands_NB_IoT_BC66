#ifndef AIR_Q_MOCK_H
#define AIR_Q_MOCK_H

#include "AtResponseCallback.h"

typedef struct
{
    char *messageToSend;
    AtResponseCallback at_response_callback;
} AirQMock;

AtResponse sendMessageOverNbIoT(char *messageToSend, AtResponseCallback at_response_callback);
void ProcessAtResponse(AtResponse *resulting_at_response);

#endif /* AIR_Q_MOCK_H */
