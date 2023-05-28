#!/usr/bin/env python3

import time
import logging
import minimalmodbus
from gateway.invoker import Invoker
from gateway.plcs import Plcs
from gateway.commands import CoilsOnCmd, CoilsOffCmd, ValidateCmd
from randomcoil import gen_coillist

PORT = '/dev/ttymxc3'
PLC_ID = 1
DELAY = 2  # Seconds

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def main() -> None:

    # port name, server address (in decimal)
    instrument1 = minimalmodbus.Instrument(PORT, PLC_ID)
    instrument1.serial.baudrate = 9600

    plc1 = Plcs(instrument1, num_coils=4)
    print(f"Connected to Plc {instrument1.address} \
        on port: {instrument1.serial.port}")

    invoker = Invoker()

    print("\nTurning off all coils [0, 0, 0, 0]")
    invoker.set_command(CoilsOffCmd(plc1, [0, 0, 0, 0]))
    invoker.invoke()
    time.sleep(DELAY)

    run = True
    while run:
        coil_list = gen_coillist(max_coils=4)
        print(f"\nTurning on random coil(s) {coil_list}")
        invoker.set_command(CoilsOnCmd(plc1, coil_list))
        invoker.invoke()

        print("\nTest coil status")
        invoker.set_command(ValidateCmd(plc1))
        invoker.invoke()
        time.sleep(DELAY)

        coil_list = gen_coillist(max_coils=4)
        print(f"\nTurning off random coil(s) {coil_list}")
        invoker.set_command(CoilsOffCmd(plc1, coil_list))
        invoker.invoke()

        print("\nTest coil status")
        invoker.set_command(ValidateCmd(plc1))
        invoker.invoke()

        time.sleep(DELAY)


if __name__ == "__main__":
    main()
