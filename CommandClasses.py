import os
from typing import Union
from StringClasses import *


class Command:

    def substitute_vars(self, envs):
        pass

    def execute(self):
        raise Exception("no specified command")


class EchoCommand(Command):

    def __init__(self, arg: Union[InterpretString | PlainString]):
        self.arg = arg

    def substitute_vars(self, envs):
        if isinstance(self.arg, InterpretString):
            if self.arg.raw_str[0] == '$':
                try:
                    value = envs[self.arg.raw_str[1:]]
                    self.arg = value
                except KeyError:
                    print("")
                return
        self.arg = self.arg.raw_str

    def execute(self):
        print(self.arg)   # TODO: ok?
