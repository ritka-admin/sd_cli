from src.str_processing.lexer import *
from src.str_processing.parser import *
from src.classes.ChannelClass import *
from src.str_processing.substitute_vars import *


def visitor(raw_user_str: str, envs: dict) -> None:
    """
    Executes users command and prints the result.

    Parameters:
        raw_user_str: command input by user
        envs: environment variables in the system
    """
    lexer_res = lexer(substitute_vars(lexer(raw_user_str), envs))

    outCh = None
    size = len(lexer_res)
    for i in range(size):
        if i == 0:
            inCh = StdChannel()
        else:
            inCh = outCh

        if i == size - 1:
            outCh = StdChannel()
        else:
            outCh = PipeChannel()
        try:
            parser_res: Command = parser(lexer_res[i])
            parser_res.execute(inCh, outCh)
        except InputError as e:
            outCh.writeline(e.msg)
        # envs = parser_res.substitute_vars(envs)
