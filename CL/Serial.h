#ifndef SERIAL_STRUCT_H
#define SERIAL_STRUCT_H
#include <windows.h>
#include "string_utils/AtString.h"

typedef struct
{
    HANDLE h_serial;
    DCB dcb_serial_params;
    COMMTIMEOUTS timeouts;
} Serial;

Serial *serial_open(const char *port, int baudrate, int timeout);
void serial_close(Serial *self);
void serial_write(Serial *self, char *data, int length);
String serial_read(Serial *self);

#endif /* SERIAL_STRUCT_H */
