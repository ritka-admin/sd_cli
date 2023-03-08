from str_processing.lexer import *
from str_processing.parser import *


def visitor(raw_user_str: str):
    input = lexer(raw_user_str)
    inCh = PypeChannel()
    outCh = PypeChannel()
    size = len(input)
    for i in range(
        0,
    ):
        inCh = outCh
        if i == 0:
            inCh = StdChannel()
        if i == size - 1:
            outCh = StdChannel()
        parser_bash(input[i]).execute(inCh, outCh)
