class PlainString:
    """
    Class for string in single quotes.
    """

    def __init__(self, raw_str: str):
        self.raw_str = raw_str


class InterpretString:
    """
    Class for string in double quotes or without quotes.
    """

    def __init__(self, raw_str: str):
        self.raw_str = raw_str
