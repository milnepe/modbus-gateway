from queue import Queue
from gateway.commands import Command

class Invoker:

    def __init__(self):
        self.cmd_queue = Queue()

    def set_command(self, cmd: Command) -> None:
        self.cmd_queue.put(cmd)

    def invoke(self) -> None:
        while not self.cmd_queue.empty():
            cmd = self.cmd_queue.get()
            cmd.execute()
