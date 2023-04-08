import os
import sys
import platform
from pathlib import Path

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
            OutCh.writeline("")
        OutCh.writeline(" ".join([el.raw_str for el in self.arg]))


class ExitCommand(Command):
    def __init__(self, arg: List[InterpretString | PlainString]):
        """
        Constructor
        Parameters:
            arg: list of InterpretString or PlainString

        """
        self.arg = None

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
        self.arg = arg

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        """
        Executes a command cat
        Parameters:
            InCh: channel to read (std::in or std::out of last command)
            OutCh: channel to write the result of execution (std::out or std::in of the next command)
        """
        if len(self.arg) == 0:
            if InCh.args:
                try:
                    byte_str = InCh.args.encode()
                    result = subprocess.run(
                        ["cat"], input=byte_str, capture_output=True
                    ).stdout.decode()
                except:
                    result = ''
                    pass
                OutCh.writeline(result)
            else:
                raise InputError("Forbidden usage of command without arguments!")
        else:
            # Creating a list of strings out of List[InterpretString | PlainString]
            result = []
            for arg in self.arg:
                result.append(
                    subprocess.run(
                        ["cat", arg.raw_str], capture_output=True
                    ).stdout.decode()
                )
            result = "".join(result)
            OutCh.writeline(result)


class WcCommand(Command):
    def __init__(self, arg: List[InterpretString | PlainString]) -> None:
        """
        Constructor
        Parameters:
            arg: list of InterpretString or PlainString
        """
        self.arg = arg

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        """
        Executes a wc command
        Parameters:
            InCh: channel to read (std::in or std::out of last command)
            OutCh: channel to write the result of execution (std::out or std::in of the next command)
        """
        if len(self.arg) == 0:
            if InCh.args:
                try:
                    byte_str = InCh.args.encode()
                    result = subprocess.run(
                        ["wc"], input=byte_str, capture_output=True
                    ).stdout.decode()
                except:
                    result = ''
                OutCh.writeline(result)
            else:
                raise InputError("Forbidden usage of command without arguments!")
        else:
            # Creating a list of strings out of List[InterpretString | PlainString]
            result = []
            for arg in self.arg:
                result.append(
                    subprocess.run(
                        ["wc", arg.raw_str], capture_output=True
                    ).stdout.decode()
                )
            result = "".join(result)
            OutCh.writeline(result)


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
        OutCh.writeline(status[1])


class LsCommand(Command):
    def __init__(self, arg: List[InterpretString | PlainString]) -> None:
        """
        Constructor
        Parameters:
            arg: list of InterpretString or PlainString
        """
        self.arg = arg

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        """
        Executes a command ls
        Parameters:
            InCh: channel to read (std::in or std::out of last command)
            OutCh: channel to write the result of execution (std::out or std::in of the next command)
        """
        try:
            result = subprocess.run(["ls", *[arg.raw_str for arg in self.arg]], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            raise InputError(e.output.decode('utf-8'))
        else:
            OutCh.writeline(result.stdout.decode('utf-8'))


class CdCommand(Command):
    def __init__(self, arg: List[InterpretString | PlainString]) -> None:
        """
        Constructor
        Parameters:
            arg: list of InterpretString or PlainString
        """
        self.arg = arg
        self.home_dir = os.environ['USERPROFILE'] if platform.system() == "Windows" else os.environ['HOME']
        self.current_directory = Path(os.getcwd())

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        """
        Executes a command cd
        Parameters:
            InCh: channel to read (std::in or std::out of last command)
            OutCh: channel to write the result of execution (std::out or std::in of the next command)
        """
        if len(self.arg) == 0:
            os.chdir(self.home_dir)
            return

        new_path = self.current_directory / Path(self.arg[0].raw_str).resolve()
        if not os.path.exists(new_path):
            raise InputError(f"cd: {new_path}: No such file or directory")
        os.chdir(new_path.as_posix().replace('/', '\\') if platform.system() == "Windows" else new_path.as_posix())