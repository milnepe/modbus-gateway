import logging
import sys
from minimalmodbus import Instrument

OFF = 0
ON = 1


class Plcs:
    """A MODBUS RTU instrument with n coils"""
    def __init__(self, instrument: Instrument, num_coils=4):
        self.instrument = instrument
        self.num_coils = num_coils
        self.coil_states = [OFF] * self.num_coils  # Remembers state of all coils

    def coils_on(self, coils: list) -> None:
        """Turn on the coils in the list"""
        self._write_coil_states(coils, ON)

    def coils_off(self, coils: list) -> None:
        """Turn off the coils in the list"""
        self._write_coil_states(coils, OFF)

    def _write_coil_states(self, coils: list, state: int) -> None:
        """Write using the MODBUS function for the coil or coils"""
        _coil_states = self.coil_states[:]  # copy coil states
        for i in coils:
            _coil_states[i] = state
            logging.debug('%s, %s', i, _coil_states[i])
        try:
            if len(coils) == 1:
                # Modbus Function Code 05: Force Single Coil (FC=05)
                self.instrument.write_bit(coils[0], _coil_states[coils[0]], functioncode=5)
                logging.info('FC05 %s %s %s', self.instrument.address, coils, _coil_states)
            else:
                # Modbus Function Code 0F: Force Multiple Coils (FC=15)
                self.instrument.write_bits(0, _coil_states)
                logging.info('FC15 %s %s %s', self.instrument.address, coils, _coil_states)
        except IOError:
            logging.error('ERROR %s: Plc%s %s %s', sys.exc_info()[0], self.instrument.address, coils, _coil_states)
        else:  # Only update if write succeeds
            self.coil_states = _coil_states

    def _read_coil_states(self) -> list:
        """Read state of all coils using MODBUS function"""
        try:
            # Modbus Function Code 01: Read Coils (FC=01)
            coil_states = self.instrument.read_bits(0, len(self.coil_states), functioncode=1)
            logging.info('FC01 %s %s', self.instrument.address, coil_states)
            return coil_states
        except IOError:
            logging.critical('ERROR %s: Plc%s', sys.exc_info()[0], self.instrument.address)
            return [-1] * self.num_coils

    def validate_coils(self):
        """Validate coil states for testing"""
        coil_states = self._read_coil_states()
        if coil_states != self.coil_states:
            logging.info('Plc %s coils invalid %s %s', self.instrument.address, coil_states, self.coil_states)
        else:
            logging.info('Plc %s coils valid %s %s', self.instrument.address, coil_states, self.coil_states)