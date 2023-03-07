import os

from classes.CommandClasses import *

from str_processing.lexer import lexer
from str_processing.parser import parser


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
