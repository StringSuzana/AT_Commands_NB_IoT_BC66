#include <string.h>
#include <stdlib.h>

#include "AtCommand.h"
#include "AtResponse.h"
#include "ResponseStatusEnum.h"
#include "ArrayUtils.h"
#include "Serial.h"

#define WAITING 0
#define NOT_FOUND -1

typedef struct
{
    char *current_response;
    char **at_response;
    int at_status;
    struct AtResponse *at_expected_response;
} Read;

// AtResponse readAtResponse(Read *self, Serial *serial, AtCommand *at_command_obj)
// {
//     char *serial_msg = fromSerial(serial);
//     int wait_intervals = at_command_obj->max_wait_for_response;

//     while (self->at_status == WAITING && wait_intervals >= 0)
//     {
//         parseMessage(self, at_command_obj, serial_msg);
//         serial_msg = fromSerial(serial);
//         wait_intervals--; // I want to sleep only 1 second at a time
//         sleep(1);
//     }
//     AtResponse r = read_answer(self->at_status, self->at_response, sizeof(self->at_response), self->at_expected_response);
//     return r;
// }
// AtResponse read_answer(Status result_status, const char **result_array, size_t result_array_len, AtResponse *at_expected_response)
// {
//     AtResponse response;
//     response.response_size = 0;
//     response.status = STATUS_ERROR;
//     response.wanted_size = 0;
//     return response;
// }
