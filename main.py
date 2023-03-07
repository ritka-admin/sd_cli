from CommandClasses import *
from StringClasses import *

from typing import List


def lexer(stdin: str) -> List[InterpretString | PlainString]:
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
        return obj_list

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

    return words_as_objs


# ----------------------------------------------------------------
context = None
command_constructors = {"echo": EchoCommand.__init__}
command_list = ["echo", "exit", "pwd", "cat", "wc"]


def parser(input: List[InterpretString | PlainString]) -> Command:

    if len(input) == 0 or input[0].raw_str.rstrip() not in command_list:
        raise Exception

    obj = EchoCommand(input[1])
    return obj
# ----------------------------------------------------------------


def main():

    envs = dict(os.environ.items())

    while True:
        command = input(">> ")

        if command == 'exit':
            break

        lexer_res = lexer(command)
        obj = parser(lexer_res)

        obj.substitute_vars(envs)
        obj.execute()


if __name__ == '__main__':
    main()
