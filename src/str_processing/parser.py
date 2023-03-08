from src.classes.CommandClass import *

context = None
command_constructors = {
    "echo": EchoCommand.__init__,
    "exit": ExitCommand.__init__,
    "pwd": PwdCommand.__init__,
    "cat": CatCommand.__init__,
    "wc": WcCommand.__init__,
}
command_list = ["echo", "exit", "pwd", "cat", "wc"]


class InputError(Exception):
    """
    Base exception for parser
    """

    def __init__(self):
        self.msg = "Command not found!"


def parser_bash(input: list) -> CommandClass:
    """
    Parses string of command to an object of CommandClass class.

    :param input: one lexem between pypes
    result: CommandClass if command is valid
    """
    if len(input) == 0 or input[0] not in command_list:
        raise InputError

    object = command_constructors[input[0]](input[0:])
    return object
