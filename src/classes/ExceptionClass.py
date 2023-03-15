class InputError(Exception):
    """
    Base exception for parser
    """

    def __init__(self, msg):
        self.msg = msg + ": команда не найдена"


class SpecialExitException(Exception):
    """
    Exception for running into "exit" command and exiting terminal.
    """

    def __init__(self):
        pass

