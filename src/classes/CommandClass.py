from abc import abstractmethod
# import sys
# sys.path.append("..")
# from classes.ChannelClass import *
# from classes.StringClass import *
from ChannelClass import *
from StringClass import *
import subprocess
from typing import Union


class Command:

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

    @abstractmethod
    def execute(self, input_channel, output_channel) -> None:
        pass


class EchoCommand(Command):
    def __init__(self, arg: Union[InterpretString | PlainString]) -> None:
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

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        """
        Executes a command echo

        :param InCh: channel to read (std::in or std::out of last command)
        :param OutCh: channel to write resul of execution (std::out or std::in of next command)
        """
        if not self.arg:
            self.arg = InCh.readline()
        OutCh.writeline(self.arg)


class ExitCommand(Command):
    def __init__(self, arg: Union[InterpretString | PlainString]) -> None:
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

    def execute(self, InCh: Channel, OutCh: Channel) -> None|Exception:
        result = subprocess.run("exit", shell=True, check=True)
        raise Exception


class PwdCommand(Command):
    def __init__(self, arg: Union[InterpretString | PlainString]) -> None:
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

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        result = subprocess.run(["pwd"], capture_output=True)
        OutCh.writeline(result.stdout.decode())


class CatCommand(Command):
    def __init__(self, arg: Union[InterpretString | PlainString]) -> None:
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

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        result = subprocess.run(["cat", self.arg],  capture_output=True)
        OutCh.writeline(result.stdout.decode())


class WcCommand(Command):
    def __init__(self, arg: Union[InterpretString | PlainString]) -> None:
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

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        result = subprocess.run(["wc", self.arg],  capture_output=True)
        OutCh.writeline(result.stdout.decode())



class VarAssignment(Command):

    def __init__(self, var, value):
        self.var = var
        self.value = value

    def substitute_vars(self, envs: dict):
        envs[self.var] = self.value

    def execute(self, input_channel=None, output_channel=None):
        pass
