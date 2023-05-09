import minimalmodbus
from gateway.invoker import Invoker
from gateway.plcs import Plcs
from gateway.commands import *
from gateway.randomcoil import *
import time
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def main() -> None:

    # port name, server address (in decimal)                                        
    instrument1 = minimalmodbus.Instrument('/dev/ttymxc3', 1)       
    instrument1.serial.baudrate = 9600
    
    plc1 = Plcs(instrument1)
    print(f"Connected to Plc {instrument1.address} \
        on port: {instrument1.serial.port}")

    invoker = Invoker()

    run = True
    while run:
        coil_list = gen_coillist(max_coils=4)
        print(f"\nTurning on random coil(s) {coil_list}")
        invoker.set_command(coils_on_cmd(plc1, coil_list))    
        invoker.invoke()
        time.sleep(2)

        print(f"\nTest coil status")        
        invoker.set_command(validate_cmd(plc1))
        invoker.invoke()        

        print(f"\nGet coil status")        
        invoker.set_command(get_states_cmd(plc1))
        invoker.invoke()        

        coil_list = gen_coillist(max_coils=4)
        print(f"\nTurning off random coil(s) {coil_list}")
        invoker.set_command(coils_off_cmd(plc1, coil_list))    
        invoker.invoke()
  
        print(f"\nTest coil status")        
        invoker.set_command(validate_cmd(plc1))
        invoker.invoke()        
        time.sleep(2)        

if __name__ == "__main__":
        main()
