from src.classes.StringClass import *
from src.classes.CommandClass import *

from typing import List


context = None
command_constructors = {
    "echo": EchoCommand,
    "exit": ExitCommand,
    "pwd": PwdCommand,
    "cat": CatCommand,
    "wc": WcCommand,
}
command_list = ["echo", "exit", "pwd", "cat", "wc"]


class InputError(Exception):
    """
    Base exception for parser
    """

    def __init__(self):
        self.msg = "Command not found!"


def parser(lexer_res: List[List[InterpretString | PlainString]]) -> Command:
    """
    Parses string of command to an object of CommandClass class.

    :param lexer_res: one lexem between pypes
    result: CommandClass if command is valid
    """
    if len(lexer_res) == 0 or lexer_res[0][0].raw_str not in command_list:      # TODO: VarAssignment
        raise InputError

    obj = command_constructors[lexer_res[0][0].raw_str](lexer_res[0][1])
    return obj
