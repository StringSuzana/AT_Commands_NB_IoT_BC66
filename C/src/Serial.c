#include <stdio.h>
#include "Serial.h"

Serial *serial_open(const char *port, int baudrate, int timeout)
{
    Serial *serial = (Serial *)malloc(sizeof(Serial));

    // Open serial port via CreateFile
    serial->hSerial = CreateFile(port,
                                 GENERIC_READ | GENERIC_WRITE,
                                 0,
                                 NULL,
                                 OPEN_EXISTING,
                                 0,
                                 NULL);

    if (serial->hSerial == INVALID_HANDLE_VALUE)
    {
        printf("CreateFile failed with error %d.\n", GetLastError());
        return (1);
    }

    // Serial port config
    GetCommState(serial->hSerial, &serial->dcbSerialParams);
    serial->dcbSerialParams.BaudRate = baudrate;
    serial->dcbSerialParams.ByteSize = 8;
    serial->dcbSerialParams.StopBits = ONESTOPBIT;
    serial->dcbSerialParams.Parity = NOPARITY;
    SetCommState(serial->hSerial, &serial->dcbSerialParams);

    // Serial port timeouts
    GetCommTimeouts(serial->hSerial, &serial->timeouts);
    serial->timeouts.ReadIntervalTimeout = timeout;
    serial->timeouts.ReadTotalTimeoutConstant = timeout;
    serial->timeouts.ReadTotalTimeoutMultiplier = 0;
    serial->timeouts.WriteTotalTimeoutConstant = timeout;
    serial->timeouts.WriteTotalTimeoutMultiplier = 0;
    SetCommTimeouts(serial->hSerial, &serial->timeouts);

    return serial;
}

void serial_close(Serial *self)
{
    CloseHandle(self->hSerial);
    free(self);
}

void serial_write(Serial *self, char *data, int length)
{
    DWORD dwBytesWritten;

    WriteFile(self->hSerial, data, length, &dwBytesWritten, NULL);

    const char *newline = "\r";
    WriteFile(self->hSerial, newline, strlen(newline), &dwBytesWritten, NULL);

    printf("serial_write dwBytesWritten: %d \n", dwBytesWritten);
    printf("serial_write length: %d \n", length);
    printf("serial_write data: %s \n", data);
}

void serial_read(Serial *self)
{
    char buffer[BUFFER_SIZE];
    DWORD dwBytesRead;

    if (ReadFile(self->hSerial, buffer, BUFFER_SIZE, &dwBytesRead, NULL))
    {
        if (dwBytesRead > 0)
        {
            printf("Read %d bytes:\n", dwBytesRead);
            for (int i = 0; i < dwBytesRead; i++)
                printf("%c", buffer[i]);
        }
    }
    else
    {
        printf("An error occured while reading from the serial port (error code %d)\n", GetLastError());
    }
}