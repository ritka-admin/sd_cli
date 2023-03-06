import os


class Command:

    def substitute_vars(self, envs):
        pass

    def execute(self):
        raise Exception("no specified command")


class EchoCommand(Command):

    def __init__(self, arg):
        self.arg = arg

    def substitute_vars(self, envs):
        if self.arg[0] == '$':
            try:
                value = envs[self.arg[1:]]
                self.arg = value
            except KeyError:
                print("")

    def execute(self):
        os.system(f'echo {self.arg}')
