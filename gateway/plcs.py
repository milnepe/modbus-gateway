from minimalmodbus import Instrument
import logging

OFF = 0
ON = 1

class Plcs:
    """A MODBUS RTU instrument with 4 coils"""
    def __init__(self, instrument: Instrument, coils=[0,1,2,3]):
        self.instrument = instrument
        self.coil_states = [OFF,OFF,OFF,OFF] # Remembers state of all coils
        self.coils: list = [] # Coil or coils to opperate on

    def coils_on(self, coils: list) -> None:
        """Turn on the coils in the list"""
        self.coils = sorted(coils)
        self.write_coil_states(ON)

    def coils_off(self, coils: list) -> None:
        """Turn off the coils in the list"""
        self.coils = sorted(coils)        
        self.write_coil_states(OFF)

    def get_states(self) -> list:
        """Get state of all coils"""
        return self.read_coil_states()

    def write_coil_states(self, state: int) -> None:
        """Write using the MODBUS function for the coil or coils"""
        for i in self.coils:
            self.coil_states[i] = state
            logging.debug(f"{i}, {self.coil_states[i]}")

        if len(self.coils) == 1:
            # Modbus Function Code 05: Force Single Coil (FC=05)
            self.instrument.write_bit(self.coils[0], self.coil_states[self.coils[0]])
            logging.info(f"FC05 {self.instrument.address} {self.coils} {self.coil_states}")            
        else:
            # Modbus Function Code 0F: Force Multiple Coils (FC=15)            
            self.instrument.write_bits(0, self.coil_states)
            logging.info(f"FC15 {self.instrument.address} {self.coils} {self.coil_states}")

    def read_coil_states(self) -> list:
        """Read the state of all coils"""
        # Modbus Function Code 01: Read Coils (FC=01)            
        coil_states = self.instrument.read_bits(0, len(self.coil_states), functioncode=1)
        logging.info(f"FC01 {self.instrument.address} {coil_states}")          
        return coil_states

    def validate(self):
        """Validate the state"""
        coil_states = self.read_coil_states()
        if coil_states != self.coil_states:
            logging.critical(f"Plc {self.instrument.address} error {coil_states} {self.coil_states}")
        else:
            logging.info(f"Plc {self.instrument.address} valid {coil_states} {self.coil_states}")                  
