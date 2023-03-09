import os
from str_processing.visitor import visitor


def main():

    envs = dict(os.environ.items())

    while True:
        command = input(">> ")
        try:
            visitor(command, envs)
        except Exception:
            break

if __name__ == '__main__':
    main()


# TODO: VarAssignment in parser `command_list`
# TODO: mark all methods as abstract methods in interfaces?
# TODO: type annotations
