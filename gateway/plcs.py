from minimalmodbus import Instrument
import logging

OFF = 0
ON = 1

class Plcs:
    """A MODBUS RTU instrument with n coils"""
    def __init__(self, instrument: Instrument, num_coils=4):
        self.instrument = instrument
        self.coil_states = [OFF] * num_coils # Remembers state of all coils

    def coils_on(self, coils: list) -> None:
        """Turn on the coils in the list"""
        self._write_coil_states(coils, ON)

    def coils_off(self, coils: list) -> None:
        """Turn off the coils in the list"""
        self._write_coil_states(coils, OFF)

    def get_states(self) -> list:
        """Get state of all coils"""
        return self._read_coil_states()

    def _write_coil_states(self, coils: list, state: int) -> None:
        """Write using the MODBUS function for the coil or coils"""
        for i in coils:
            self.coil_states[i] = state
            logging.debug(f"{i}, {self.coil_states[i]}")
        if len(coils) == 1:
            # Modbus Function Code 05: Force Single Coil (FC=05)
            self.instrument.write_bit(coils[0], self.coil_states[coils[0]])
            logging.info(f"FC05 {self.instrument.address} {coils} {self.coil_states}")            
        else:
            # Modbus Function Code 0F: Force Multiple Coils (FC=15)            
            self.instrument.write_bits(0, self.coil_states)
            logging.info(f"FC15 {self.instrument.address} {coils} {self.coil_states}")

    def _read_coil_states(self) -> list:
        """Read the state of all coils"""
        # Modbus Function Code 01: Read Coils (FC=01)            
        coil_states = self.instrument.read_bits(0, len(self.coil_states), functioncode=1)
        logging.info(f"FC01 {self.instrument.address} {coil_states}")          
        return coil_states

    def validate_coils(self):
        """Validate the state"""
        coil_states = self._read_coil_states()
        if coil_states != self.coil_states:
            logging.critical(f"Plc {self.instrument.address} error {coil_states} {self.coil_states}")
        else:
            logging.info(f"Plc {self.instrument.address} valid {coil_states} {self.coil_states}")                  
