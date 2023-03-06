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

    met_unary = False
    met_binary = False
    cur_u = 0
    cur_b = 0
    index = 0
    unary_words = []
    binary_words = []
    for word in words:

        if word == "'":
            if not met_unary:
                met_unary = True
                unary_words.append(['', index])
                index += 1
            else:
                met_unary = False
                cur_u += 1
            continue

        elif word == '"':
            if not met_binary:
                met_binary = True
                binary_words.append(['', index])
                index += 1
            else:
                met_binary = False
                cur_b += 1
            continue

        if met_unary:
            unary_words[cur_u][0] += word

        elif met_binary:
            binary_words[cur_b][0] += word

        elif not met_unary and not met_binary:
            binary_words.append([word, index])
            cur_b += 1
            index += 1

    # TODO: if quote is not closed -- read further

    for u in range(len(unary_words)):
        prev = unary_words[u]       # list of two elements
        unary_words[u] = (PlainString(prev[0]), prev[1])

    for b in range(len(binary_words)):
        prev = binary_words[b]
        binary_words[b] = (InterpretString(prev[0]), prev[1])

    real_words = unary_words + binary_words
    r_words_sorted = sorted(real_words, key=lambda x: x[1])
    ret = [word[0] for word in r_words_sorted]
    return ret   # TODO: ?????

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
