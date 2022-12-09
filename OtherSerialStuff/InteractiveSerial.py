import sys
import getopt
import os
import time
import io
import serial as serial
from colorama import Fore

AT_QBAND_GET = "AT+QBAND?"
AT_GET = "AT"


if __name__ == '__main__':

    ser = serial.Serial(port="COM10", baudrate=9600, timeout=600)
    ser.isOpen()
    input_command = 1
    print("Enter commands [E for Exit]")
    while input_command:
        input_command = input(">>")
        if input_command.capitalize() == "E":
            ser.close()
            exit()
        else:
            ser.write((input_command + '\r').encode('ASCII'))
            out = ''
            time.sleep(1)
            while ser.in_waiting > 0:
                out += ser.read(1).decode('ASCII')
            if out != '':
                print(">> " + out)
                print(ser.timeout)
