import sys

sys.path.append("..")
from str_processing.lexer import *
from str_processing.parser import *
from str_processing.substitute_vars import *

# from src.str_processing.lexer import *
# from src.str_processing.parser import *


def visitor(raw_user_str: str, envs: dict) -> None:
    """
    Executes users command and writes it.

    Parameters:
        raw_user_str: command typed by user
        envs: environment variables in system
    """
    lexer_res = lexer(substitute_vars(lexer(raw_user_str),envs))
    # lexer_res = lexer(raw_user_str)

    size = len(lexer_res)
    for i in range(size):
        if i == 0:
            inCh = StdChannel()
        else:
            inCh = PipeChannel()

        if i == size - 1:
            outCh = StdChannel()
        else:
            outCh = PipeChannel()
        parser_res: Command = parser(lexer_res[i])
        # envs = parser_res.substitute_vars(envs)
        parser_res.execute(inCh, outCh)
