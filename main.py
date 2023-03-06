from CommandClasses import *
from StringClasses import *

import subprocess
from typing import List
envs = dict()


def collect_vars():
    output = subprocess.check_output('printenv', shell=True).decode()
    output_list = output.split('\n')
    for elem in output_list:
        key, *value = elem.split('=')     # TODO: splitting by '=' produces more than 2 values sometimes
        envs[key] = value


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
            binary_words.append([word, index])          # TODO: map? word.rstrip?
            cur_b += 1
            index += 1

    # TODO: if quote is not closed -- read further

    for u in range(len(unary_words)):
        prev = unary_words[u]       # list of two elements
        unary_words[u] = [PlainString(prev[0]), prev[1]]

    for b in range(len(binary_words)):
        prev = binary_words[b]
        binary_words[b] = [InterpretString(prev[0]), prev[1]]

    real_words = unary_words + binary_words
    r_words_sorted = sorted(real_words, key=lambda x: x[1])
    ret = [word[0] for word in r_words_sorted]
    return ret   # TODO: ?????


def parser(lexer_res: List[InterpretString | PlainString]):
    if lexer_res[0].raw_str.rstrip() == 'echo':
        x = EchoCommand(lexer_res[1].raw_str)
        return x
    else:
        return Command()


def main():

    collect_vars()

    while True:
        command = input(">> ")

        if command == 'exit':
            break

        lexer_res = lexer(command)
        obj = parser(lexer_res)

        obj.execute()


if __name__ == '__main__':
    main()
