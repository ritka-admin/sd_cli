from abc import abstractmethod
from classes.ChannelClass import *


class CommandClass:
    def __init__(self, args: str) -> None:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass


class EchoCommand(CommandClass):
    def __init__(self, args: str = None) -> None:
        self.args = args

    def execute(self, InCh: Channel, OutCh: Channel) -> None:
        """
        Executes a command echo

        :param InCh: channel to read (std::in or std::out of last command)
        :param OutCh: channel to write resul of execution (std::out or std::in of next command)
        """
        if not self.args:
            self.args = InCh.readline()
        OutCh.writline(self.args)


class ExitCommand(CommandClass):
    def __init__(self, args: str) -> None:
        self.args = args

    def execute_(self) -> None:
        pass


class PwdCommand(CommandClass):
    def __init__(self, args: str) -> None:
        self.args = args

    def execute(self) -> None:
        pass


class CatCommand(CommandClass):
    def __init__(self, args: str) -> None:
        self.args = args

    def execute(self) -> None:
        pass


class WcCommand(CommandClass):
    def __init__(self, args: str) -> None:
        self.args = args

    def execute(self) -> None:
        pass
