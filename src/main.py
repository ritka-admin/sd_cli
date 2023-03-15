import os
from src.str_processing.visitor import visitor
from src.classes.ExceptionClass import SpecialExitException, InputError


def main():
    """
    Main function for reading users commands and executing them.
    """
    envs = dict(os.environ.items())
    envs["x"]="ex"
    envs["y"]="it"

    while True:
        command = input(">> ")
        try:
            visitor(command, envs)
        except InputError:
            print("Invalid command")
        except SpecialExitException:
            break


if __name__ == "__main__":
    main()