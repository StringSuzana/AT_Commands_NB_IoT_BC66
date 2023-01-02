#include <stdio.h>
#include "Serial.h"
#include <stdlib.h>

Serial *serial_open(const char *port, int baudrate, int timeout)
{
    Serial *serial = (Serial *)malloc(sizeof(Serial));

    // Open serial port via CreateFile
    serial->h_serial = CreateFile(port,
                                  GENERIC_READ | GENERIC_WRITE,
                                  0,
                                  NULL,
                                  OPEN_EXISTING,
                                  0,
                                  NULL);

    if (serial->h_serial == INVALID_HANDLE_VALUE)
    {
        printf("CreateFile failed with error %d.\n", GetLastError());
        return (1);
    }

    // Serial port config
    GetCommState(serial->h_serial, &serial->dcb_serial_params);
    serial->dcb_serial_params.BaudRate = baudrate;
    serial->dcb_serial_params.ByteSize = 8;
    serial->dcb_serial_params.StopBits = ONESTOPBIT;
    serial->dcb_serial_params.Parity = NOPARITY;
    SetCommState(serial->h_serial, &serial->dcb_serial_params);

    // Serial port timeouts
    GetCommTimeouts(serial->h_serial, &serial->timeouts);
    serial->timeouts.ReadIntervalTimeout = timeout;
    serial->timeouts.ReadTotalTimeoutConstant = timeout;
    serial->timeouts.ReadTotalTimeoutMultiplier = 0;
    serial->timeouts.WriteTotalTimeoutConstant = timeout;
    serial->timeouts.WriteTotalTimeoutMultiplier = 0;
    SetCommTimeouts(serial->h_serial, &serial->timeouts);

    return serial;
}

void serial_close(Serial *self)
{
    CloseHandle(self->h_serial);
    free(self);
}

void serial_write(Serial *self, char *data, int length)
{
    DWORD dwBytesWritten;

    WriteFile(self->h_serial, data, length, &dwBytesWritten, NULL);

    const char *newline = "\r";
    WriteFile(self->h_serial, newline, strlen(newline), &dwBytesWritten, NULL);

    printf("serial_write dwBytesWritten: %d \n", dwBytesWritten);
    printf("serial_write length: %d \n", length);
    printf("serial_write data: %s \n", data);
}

char *serial_read(Serial *self)
{
    char buffer[BUFFER_SIZE];
    DWORD dwBytesRead;

    if (ReadFile(self->h_serial, buffer, BUFFER_SIZE, &dwBytesRead, NULL))
    {
        if (dwBytesRead > 0)
        {
            printf("Read %d bytes:\n", dwBytesRead);
            for (int i = 0; i < dwBytesRead; i++)
            {
                printf("%c", buffer[i]);
            }
            return buffer;
        }
    }
    else
    {
        printf("An error occured while reading from the serial port (error code %d)\n", GetLastError());
    }
}