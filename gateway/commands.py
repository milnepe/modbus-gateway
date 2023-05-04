from gateway.coil import Coils

class Command:
    def execute(self):
        pass

class coils_on_cmd(Command):

    def __init__(self, coils: list):
        self.coils = coils

    def execute(self) -> None:
        self.coils.coils_on()

class coils_off_cmd(Command):

    def __init__(self, coils: list):
        self.coils = coils

    def execute(self) -> None:
        self.coils.coils_off()
