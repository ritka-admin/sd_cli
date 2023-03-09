import os

from classes.CommandClass import *

from str_processing.lexer import lexer
from str_processing.parser import parser
from str_processing.visitor import visitor


def main():

    envs = dict(os.environ.items())

    while True:
        command = input(">> ")

        visitor(command, envs)

        # if command == 'exit':
        #     break
        #
        # lexer_res = lexer(command)
        # obj = parser(lexer_res)
        #
        # obj.substitute_vars(envs)
        # obj.execute()


if __name__ == '__main__':
    main()


# `parser` insted of `parser_bash`
# VarAssignment in parser `command_list`
# __init__ in the interfaces (not needed)
# how to use visitor?
# mark all methods as abstract methods in interfaces?
# TODO: type annotations
