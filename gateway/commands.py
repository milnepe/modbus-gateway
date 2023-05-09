from gateway.plcs import Plcs

class Command:
    def execute(self):
        pass

class coils_on_cmd(Command):
    def __init__(self, plc: Plcs, coil_list: list):
        self.plc = plc
        self.coil_list = coil_list

    def execute(self) -> None:
        self.plc.coils_on(self.coil_list)

class coils_off_cmd(Command):
    def __init__(self, plc: Plcs, coil_list: list):
        self.plc = plc
        self.coil_list = coil_list        

    def execute(self) -> None:
        self.plc.coils_off(self.coil_list)

class validate_cmd(Command):
    def __init__(self, plc: Plcs):
        self.plc = plc

    def execute(self) -> None:
        self.plc.validate_coils()