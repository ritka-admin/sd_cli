from src.classes.CommandClass import *
from src.classes.StringClass import *

from typing import List


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
        lex_str: list of lexical tokens of a command between pipes
    Returns:
        CommandClass object if the command is valid
    """
    if len(lex_str) == 0:
        return EchoCommand([PlainString('')])
    elif lex_str[0].raw_str not in command_list:
        return ExternalCommand(lex_str[0].raw_str)

    obj = command_constructors[lex_str[0].raw_str](lex_str[1:])
    return obj
