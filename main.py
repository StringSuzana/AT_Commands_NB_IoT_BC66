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

# ser = serial.Serial(port="COM10", baudrate=9600,)
# ser.write(b"AT+QBAND?\r")

if __name__ == '__main__':
    with serial.serial_for_url('spy://COM10?file=test.txt', timeout=1) as s:
        print(f"On port : {s.name}")
        s.write(b'AT\r')
        s.write(b'AT+CGMI\r')
        time.sleep(1)
        s.write(b"AT+QBAND?\r\n")
        time.sleep(1)

        s.write(b"AT+QSOCON=?\r")
        #s.write(b"AT+QSOC=1,2,1\r")

        byte_lines = s.readlines()
        lines = [x[0:-2] for x in byte_lines]
        # lines_array = [y.split() for y in lines]
        [print(f" {y} ") for y in lines]

        #[print(f"{Fore.GREEN} {y} ") for y in lines]

        s.send_break()
