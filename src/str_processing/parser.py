from src.classes.CommandClasses import *

from typing import List


context = None
command_constructors = {"echo": EchoCommand.__init__}
command_list = ["echo", "exit", "pwd", "cat", "wc"]   # VarAssignment?


def parser(input_lst: List[InterpretString | PlainString]) -> Command:

    if len(input_lst) == 0:
        raise Exception

    if input_lst[0].raw_str == 'echo':
        obj = EchoCommand(input_lst[1])
    else:
        var, value = input_lst[0].raw_str.split("=")
        obj = VarAssignment(var, value)
    return obj
