import minimalmodbus
from gateway.invoker import Invoker
from gateway.coil import Coils
from gateway.randomcoil import *
from gateway.commands import *
import time

def main() -> None:
    # port name, server address (in decimal)                                        
    instrument1 = minimalmodbus.Instrument('/dev/ttymxc3', 1)       
    instrument1.serial.baudrate = 9600
    print(f"Connected to server {instrument1.address} \
        on port: {instrument1.serial.port}")

    invoker = Invoker()

    run = True
    while run:
        coil_list = [0, 1, 2, 3]
        print(f"Turning off all coils {coil_list}")
        invoker.set_command(coils_off_cmd(Coils(instrument1, coil_list)))
        invoker.invoke()
        time.sleep(2)

        coil_list = gen_coillist(max_coils=4)
        print(f"Turning on random coil(s) {coil_list}")
        invoker.set_command(coils_on_cmd(Coils(instrument1, coil_list)))    
        invoker.invoke()
        time.sleep(2)

        coil_list = [0, 1, 2, 3]
        print(f"Turning on all coils {coil_list}")
        invoker.set_command(coils_on_cmd(Coils(instrument1, coil_list)))
        invoker.invoke()
        time.sleep(2)

        coil_list = gen_coillist(max_coils=4)
        print(f"Turning off random coil(s) {coil_list}")
        invoker.set_command(coils_off_cmd(Coils(instrument1, coil_list)))    
        invoker.invoke()
        time.sleep(2)

if __name__ == "__main__":
        main()
