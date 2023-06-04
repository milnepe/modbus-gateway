#!/usr/bin/env python3

import time
import logging
import minimalmodbus
from gateway.invoker import Invoker
from gateway.plcs import Plcs
from gateway.commands import TimerSetCmd, ResetTimersCmd

PORT = '/dev/ttymxc3'
PLC_ID = 1

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def main() -> None:

    # port name, server address (in decimal)
    instrument1 = minimalmodbus.Instrument(PORT, PLC_ID)
    instrument1.serial.baudrate = 9600

    plc1 = Plcs(instrument1, num_coils=4)
    print(f"Connected to Plc {instrument1.address} \
        on port: {instrument1.serial.port}")

    invoker = Invoker()

    print("\nSet timers T1, T2, T3, T4 in mode 10")
    invoker.set_command(TimerSetCmd(plc1, 0, [10, 0, 0, 10])) # T1
    invoker.set_command(TimerSetCmd(plc1, 4, [20, 0, 0, 10])) # T2
    invoker.set_command(TimerSetCmd(plc1, 8, [10, 0, 0, 10])) # T3
    invoker.set_command(TimerSetCmd(plc1, 12, [20, 0, 0, 10])) # T4

    invoker.invoke()

    time.sleep(10)

    print("\nReset Timers")
    invoker.set_command(ResetTimersCmd(plc1))

    invoker.invoke()

if __name__ == "__main__":
    main()
