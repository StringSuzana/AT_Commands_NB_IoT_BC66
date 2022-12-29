#ifndef SERIAL_STRUCT_H
#define SERIAL_STRUCT_H
#include <windows.h>

#define BUFFER_SIZE 1024

// Structure to store the serial port handle and configuration
typedef struct
{
    HANDLE hSerial;
    DCB dcbSerialParams;
    COMMTIMEOUTS timeouts;
} Serial;

// Function prototypes
Serial *serial_open(const char *port, int baudrate, int timeout);
void serial_close(Serial *self);
void serial_write(Serial *self, const char *data, int length);
void serial_read(Serial *self);

#endif /* SERIAL_STRUCT_H */
