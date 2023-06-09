from gateway.plcs import Plcs


class Command:
    def execute(self):
        raise NotImplementedError


class CoilsOnCmd(Command):
    def __init__(self, plc: Plcs, coil_list: list):
        self.plc = plc
        self.coil_list = coil_list

    def execute(self) -> None:
        if self.plc is not None:
            self.plc.coils_on(self.coil_list)


class CoilsOffCmd(Command):
    def __init__(self, plc: Plcs, coil_list: list):
        self.plc = plc
        self.coil_list = coil_list

    def execute(self) -> None:
        if self.plc is not None:
            self.plc.coils_off(self.coil_list)


class ValidateCmd(Command):
    def __init__(self, plc: Plcs):
        self.plc = plc

    def execute(self) -> None:
        if self.plc is not None:
            self.plc.validate_coils()


class TimerSetCmd(Command):
    def __init__(self, plc: Plcs, start_address: int, values: list):
        self.plc = plc
        self.start_address = start_address
        self.values = values

    def execute(self) -> None:
        if self.plc is not None:
            self.plc.timer_set(self.start_address, self.values)


class ResetTimersCmd(Command):
    def __init__(self, plc: Plcs):
        self.plc = plc

    def execute(self) -> None:
        if self.plc is not None:
            self.plc.reset_timers()
