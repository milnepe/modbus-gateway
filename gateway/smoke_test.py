#!/usr/bin/env python3
from time import sleep
import minimalmodbus as mm

ON = 1
OFF = 0

plc = mm.Instrument('/dev/ttymxc3', 1)
plc.serial.baudrate = 9600

while True:
    # Toggle outputs Q1 - Q4 in sequence
    for coil in range(0, 4):
        plc.write_bit(coil, ON, functioncode=5)
        print(f'Q{coil + 1}, {plc.read_bit(coil, functioncode=1)}')
        sleep(1)
        plc.write_bit(coil, OFF, functioncode=5)
        print(f'Q{coil + 1}, {plc.read_bit(coil, functioncode=1)}')
        sleep(1)
