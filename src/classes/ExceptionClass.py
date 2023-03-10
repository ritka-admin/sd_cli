
class InputError(Exception):
    """
    Base exception for parser
    """

    def __init__(self):
        self.msg = "Command not found!"


class SpecialExitException(Exception):

    def __init__(self):
        pass

