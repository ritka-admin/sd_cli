import os
from str_processing.visitor import visitor
from src.classes.ExceptionClass import SpecialExitException, InputError


def main():

    envs = dict(os.environ.items())

    while True:
        command = input(">> ")
        try:
            visitor(command, envs)
        except InputError:
            print("Invalid command")
        except SpecialExitException:
            break


if __name__ == '__main__':
    main()


# TODO: mark all methods as abstract methods in interfaces?
