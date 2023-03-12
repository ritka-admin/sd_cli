import sys

sys.path.append("..")
from classes.CommandClass import *
from classes.ExceptionClass import *

# from src.classes.CommandClass import *
# from src.classes.ExceptionClass import InputError

from typing import List


context = None
command_constructors = {
    "echo": EchoCommand,
    "exit": ExitCommand,
    "pwd": PwdCommand,
    "cat": CatCommand,
    "wc": WcCommand,
    "=": VarAssignment,
}
command_list = ["echo", "exit", "pwd", "cat", "wc", "="]


def parser(lex_str: List[InterpretString | PlainString]) -> Command:
    """
    Parses string of command to an object of CommandClass class.

    Parameters:
        lex_str: one lexem between pypes
    Returns:
        CommandClass if command is valid
    """
    if len(lex_str) == 0 or lex_str[0].raw_str not in command_list:
        raise InputError

    obj = command_constructors[lex_str[0].raw_str](lex_str[1:])
    return obj
