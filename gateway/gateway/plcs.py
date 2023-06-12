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
        self.timer_states = {}

    def coils_on(self, coils: list) -> None:
        """Turn on the coils in the list"""
        self._write_coils(coils, ON)

    def coils_off(self, coils: list) -> None:
        """Turn off the coils in the list"""
        self._write_coils(coils, OFF)

    def validate_coils(self):
        """Validate coil states for testing"""
        coil_states = self._coils_read()
        if coil_states != self.coil_states:
            logging.info('Plc %s coils invalid %s %s', self.instrument.address, coil_states, self.coil_states)
        else:
            logging.info('Plc %s coils valid %s %s', self.instrument.address, coil_states, self.coil_states)

    def timer_set(self, start_address: int, values: list) -> None:
        """Set timer holding registers
        Each timer has 4 registers:
            Timer preset off time
            Timer preset on time
            Timer resolution
            Timer mode
        """
        self._timer_save(start_address)  # Save current values
        self._write_registers(start_address, values)  # Write new values

    def reset_timers(self):
        """Reset timer values"""
        for start_address, values in self.timer_states.items():
            self._write_registers(start_address, values)

    def _timer_save(self, start_address) -> None:
        """Save timers holding register"""
        number_of_registers = 4
        try:
            timer = {start_address: self.instrument.read_registers(start_address, number_of_registers, functioncode=3)}
        except Exception:
            logging.error('ERROR %s: Plc%s %s %s', sys.exc_info()[0], self.instrument.address, start_address, number_of_registers)
        else:
            self.timer_states.update(timer)  # Stash timer values

    def _write_coils(self, coils: list, state: int) -> None:
        """Write using the MODBUS function for the coil or coils in list"""
        _coil_states = self._coils_read()  # Read current state of all coils
        for i in coils:
            _coil_states[i] = state  # Update each coil in coils list
        try:
            if len(coils) == 1:
                # Modbus Function Code 05: Force Single Coil (FC=05)
                self.instrument.write_bit(coils[0], state, functioncode=5)
                logging.info('FC05 %s %s %s', self.instrument.address, coils, _coil_states)
            else:
                # Modbus Function Code 0F: Force Multiple Coils (FC=15)
                self.instrument.write_bits(0, _coil_states)
                logging.info('FC15 %s %s %s', self.instrument.address, coils, _coil_states)
        except Exception:
            logging.error('ERROR %s: Plc%s %s %s', sys.exc_info()[0], self.instrument.address, coils, _coil_states)
        else:
            self.coil_states = _coil_states[:]  # Save new states

    def _coils_read(self) -> list:
        """Return state of all coils using MODBUS function code 01"""
        try:
            _coil_states = self.instrument.read_bits(0, self.num_coils, functioncode=1)
            logging.info('FC01 %s %s', self.instrument.address, _coil_states)
            return _coil_states
        except Exception:
            logging.critical('ERROR %s: Plc%s', sys.exc_info()[0], self.instrument.address)
            return [-1] * self.num_coils

    def _write_registers(self, start_address: int, values: list) -> None:
        """Write holding registers using MODBUS function code 16
        The number of registers is defined by the size of the list"""
        try:
            self.instrument.write_registers(start_address, values)
            logging.info('FC16 Plc:%s Address:%s Values:%s', self.instrument.address, start_address, values)
        except IOError:
            logging.error('ERROR %s: Plc%s %s %s', sys.exc_info()[0], self.instrument.address, start_address, values)
