import sys

from src.classes.ChannelClass import *
from src.classes.StringClass import *
from src.classes.ExceptionClass import *
import subprocess
from typing import Union, List


class Command:
    """
    Abstract class for commands to execute them.
    """
    @abstractmethod
    def execute(self, input_channel: Channel, output_channel: Channel) -> None:
        pass


class EchoCommand(Command):
    """
    Class for command echo to execute a command with its arguments.
    """

    def __init__(self, arg: List[InterpretString | PlainString]):
        """
        Constructor
        Parameters:
            arg: list of InterpretString or PlainString
        """
        self.arg = arg


    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        """
        Executes a command echo
        Parameters:
            InCh: channel to read (std::in or std::out of the last command)
            OutCh: channel to write the result of execution (std::out or std::in of the next command)
        """
        if not self.arg:
            self.arg = InCh.readline()
        OutCh.writeline(''.join([el.raw_str for el in self.arg]))


class ExitCommand(Command):
    def __init__(self, arg: List[InterpretString | PlainString]):
        """
        Constructor
        Parameters:
            arg: list of InterpretString or PlainString

        """
        self.arg = None

    # def substitute_vars(self, envs):
    #     pass

    def execute(self, InCh: Channel, OutCh: Channel) -> None | SpecialExitException:
        """
        Executes a command exit
        Parameters:
            InCh: channel to read (std::in or std::out of last command)
            OutCh: channel to write the result of execution (std::out or std::in of the next command)
        """
        raise SpecialExitException


class PwdCommand(Command):
    def __init__(self, arg: List[InterpretString | PlainString]) -> None:
        """
        Constructor
        Parameters:
            arg: list of InterpretString or PlainString
        """
        self.arg = None

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        """
        Executes a command pwd
        Parameters:
            InCh: channel to read (std::in or std::out of last command)
            OutCh: channel to write the result of execution (std::out or std::in of the next command)
        """
        result = subprocess.run(["pwd"], capture_output=True)
        OutCh.writeline(result.stdout.decode())


class CatCommand(Command):
    def __init__(self, arg: List[InterpretString | PlainString]) -> None:
        """
        Constructor
        Parameters:
            arg: list of InterpretString or PlainString
        """
        (self.arg,) = arg

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        """
        Executes a command cat
        Parameters:
            InCh: channel to read (std::in or std::out of last command)
            OutCh: channel to write the result of execution (std::out or std::in of the next command)
        """
        result = subprocess.run(["cat", self.arg], capture_output=True)
        OutCh.writeline(result.stdout.decode())


class WcCommand(Command):
    def __init__(self, arg: List[InterpretString | PlainString]) -> None:
        """
        Constructor
        Parameters:
            arg: list of InterpretString or PlainString
        """
        (self.arg,) = arg

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        """
        Executes a wc command
        Parameters:
            InCh: channel to read (std::in or std::out of last command)
            OutCh: channel to write the result of execution (std::out or std::in of the next command)
        """
        result = subprocess.run(["wc", self.arg], capture_output=True)
        OutCh.writeline(result.stdout.decode())


class VarAssignment(Command):
    def __init__(self, args: List[InterpretString | PlainString]) -> None:
        """
        Constructor
        Parameters:
            args: list of InterpretString or PlainString
        """
        self.args = args
        self.var = args[0].raw_str
        self.value = args[1].raw_str

    # def substitute_vars(self, envs: dict):
    #     envs[self.var] = self.value

    def execute(self, InCh=None, OutCh=None):
        """
        Executes a variable assignment command
        Parameters:
            InCh: channel to read (std::in or std::out of last command)
            OutCh: channel to write the result of execution (std::out or std::in of the next command)
        """
        pass


class ExternalCommand(Command):

    def __init__(self, arg):
        self.arg = arg

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        status = subprocess.getstatusoutput(self.arg)
        if status[0] != 0:
            raise InputError(self.arg)
        # result = subprocess.run(self.arg, capture_output=True)
        OutCh.writeline(status[1])
