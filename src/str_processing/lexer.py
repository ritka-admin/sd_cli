from src.classes.StringClass import *

from typing import List


def lexer(stdin: str) -> List[List[InterpretString | PlainString]]:
    """
    :param stdin:

    Returns:
      if there is a pipe in a raw_command, parser will need
      separate commands as separate lists
    """
    words = []

    start = 0
    for i in range(len(stdin)):

        if stdin[i] == "'":
            words.append(stdin[start:i])
            start = i + 1
            words.append("'")

        elif stdin[i] == '"':
            words.append(stdin[start:i])
            start = i + 1
            words.append('"')

    # if there are no quotes in stdin
    if not start and len(stdin):
        words = stdin.split()
        obj_list = []
        for i in range(len(words)):
            obj = InterpretString(words[i])
            obj_list.append(obj)
        lexer_res = []
        lexer_res.append(obj_list)
        return lexer_res

    met_mark = None
    quotes = ["'", '"']
    words_as_objs = []
    elem = ''

    for word in words:

        if met_mark is None and word in quotes:
            if elem:
                obj = InterpretString(elem.rstrip())
                words_as_objs.append(obj)
                elem = ''
            met_mark = word
            continue

        elif word == met_mark:
            if met_mark == "'":
                obj = PlainString(elem.rstrip())
            else:
                obj = InterpretString(elem.rstrip())

            words_as_objs.append(obj)
            elem = ''
            met_mark = None
            continue

        elem += word

    # TODO: if quote is not closed -- read further

    lexer_res = []
    lexer_res.append(words_as_objs)

    return lexer_res
