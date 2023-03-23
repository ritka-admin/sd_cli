from src.classes.StringClass import *

from typing import List


def lexer(stdin: str, prev_res=None, mark=None, skip=False) -> List[List[InterpretString | PlainString]]:
    """
    Parameters:
        stdin: raw string from stdin
        prev_res: auxiliary information for multistring processing
        mark: auxiliary information for multistring processing (the mark that was left unclosed)
        skip: auxiliary information for splitting by pipe

    Returns:
      List of several lists with InterpretString / PlainString objects.
      If there is a pipe in a raw command, parser will need
      separate commands as separate lists
    """
    if not skip:
        commands = stdin.split('|')
        result = []
        for cmd in commands:
            res = lexer(cmd, skip=True)
            result.extend(res)
        return result

    words = [] if prev_res is None else prev_res
    met_mark = None if mark is None else mark

    start = 0
    for i in range(len(stdin)):

        prev = max(0, i-1)

        if stdin[i] == "'" and met_mark is None and stdin[prev] == " ":
            if i != 0:
                words.append(InterpretString(stdin[start:i]))
            start = i + 1
            met_mark = "'"

        elif stdin[i] == '"' and met_mark is None and stdin[prev] == " ":
            if i != 0:
                words.append(InterpretString(stdin[start:i]))
            start = i + 1
            met_mark = '"'

        elif stdin[i] == met_mark:
            if met_mark == "'":
                words.append(PlainString(stdin[start:i]))
            else:
                words.append(InterpretString(stdin[start:i]))
            start = i + 1
            met_mark = None

    # if no quote was met
    if met_mark is None and len(words) == 0:
        words = stdin.split()
        obj_list = [InterpretString(obj) for obj in words]
        return [obj_list]

    if met_mark is not None:
        inner = PlainString(stdin[start:]) if met_mark == "'" else InterpretString(stdin[start:])
        words.append(inner)
        res = lexer(input(), words, met_mark, skip=True)
        return res

    lexer_res = [words]
    return lexer_res

