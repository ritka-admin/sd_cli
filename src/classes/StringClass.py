class PlainString:
    """
    Class for a string in single quotes.
    """

    def __init__(self, raw_str):
        self.raw_str = raw_str


class InterpretString:
    """
    Class for a string in double quotes or without quotes.
    """

    def __init__(self, raw_str):
        self.raw_str = raw_str
