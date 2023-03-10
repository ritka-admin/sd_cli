from src.str_processing.lexer import *
from src.str_processing.parser import *


def visitor(raw_user_str: str, envs: dict) -> None:
    lexer_res = lexer(raw_user_str)
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
        envs = parser_res.substitute_vars(envs)
        parser_res.execute(inCh, outCh)
