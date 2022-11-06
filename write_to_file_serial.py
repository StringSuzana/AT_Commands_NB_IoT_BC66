import sys
import getopt
import os
import time
import json
import io
import serial as serial
from colorama import Fore
from colorama import Style
from collections import deque

if __name__ == '__main__':

    with serial.serial_for_url('spy://COM10?file=logs/test.txt', timeout=1) as s:
        print(f"On port : {s.name}")
        s.write(b'AT\r')
        s.write(b'AT+CGMI\r')  # Request Manufacturer Identification
        time.sleep(1)
        s.write(b"AT+QBAND?\r\n")  # query available bands
        time.sleep(1)

        s.write(b"AT+QSOCON=?\r")  # list of available socket ids, remote address and ports
        # s.write(b"AT+QSOC=1,2,1\r") #connect socket to remote address and port
        s.write(b"AT+QENGINFO=?\r")  # query current modem status information

        byte_lines = s.readlines()

        lines = [x[0:-2] for x in byte_lines]
        # lines_array = [y.split() for y in lines]
        [print(f"{Fore.GREEN} {y} ") for y in lines]

        s.send_break()