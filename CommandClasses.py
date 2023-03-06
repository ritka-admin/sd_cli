import os


class Command:

    def substitute_vars(self):
        pass

    def execute(self):
        raise Exception("no specified command")


class EchoCommand(Command):

    def __init__(self, arg):
        self.arg = arg          # TODO: different fields for different argument types?

    def substitute_vars(self):
        pass

    def execute(self):
        os.system(f'echo {self.arg}')
