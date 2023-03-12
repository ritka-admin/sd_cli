class InputError(Exception):
    """
    Base exception for parser
    """

    def __init__(self):
        self.msg = "Command not found!"


class SpecialExitException(Exception):
    """
    Exception for meeting an "exit" command and exiting terminal.
    """

    def __init__(self):
        pass
