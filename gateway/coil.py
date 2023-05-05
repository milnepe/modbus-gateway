from minimalmodbus import Instrument
import logging

OFF = 0
ON = 1

class Coils:
    """Represents the coils or list of coils to operate on attached to an
    instrument"""

    coil_states = [OFF,OFF,OFF,OFF] # Remembers state of all coils

    def __init__(self, instrument: Instrument, coils: list):
        self.instrument = instrument
        self.coils: list = sorted(coils) # Coil or coils to opperate on

    def coils_on(self) -> None:
        """Turn on the specific coil or list of coils"""
        self.set_coil_states(ON)
        self.write_coil_states(ON)

    def coils_off(self) -> None:
        """Turn off the specific coil or list of coils"""
        self.set_coil_states(OFF)
        self.write_coil_states(OFF)        

    def set_coil_states(self, state: int) -> None:
        """Set the state for the specific coil or list of coils"""
        for i in self.coils:
            self.coil_states[i] = state
            logging.debug(f"{i}, {self.coil_states[i]}")

    def write_coil_states(self, state: int) -> None:
        """Perform the Modbus function for the coil or list of coils"""
        if len(self.coils) == state:
            # Modbus Function Code 05: Single Coil (FC=05)
            self.instrument.write_bit(self.coils[0], self.coil_states[self.coils[0]])
            logging.info(f"FC05 {self.instrument.address} {self.coils} {self.coil_states}")            
        else:
            # Modbus Function Code 0F: Multiple Coils (FC=15)            
            self.instrument.write_bits(0, self.coil_states)
            logging.info(f"FC15 {self.instrument.address} {self.coils} {self.coil_states}")             
