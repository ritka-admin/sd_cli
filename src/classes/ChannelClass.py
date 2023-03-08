from abc import abstractmethod


class Channel:
    def __init__(self):
        pass

    @abstractmethod
    def readline(self) -> str:
        pass

    def writline(self, string: str):
        pass


class StdChannel(Channel):
    def __init__(self):
        pass

    def readline(self) -> str:
        strline = input()
        return strline

    def writline(self, string: str):
        print(string)


class PypeChannel(Channel):
    def __init__(self):
        self.args = None

    def readline(self):
        return self.args

    def writline(self, string: str):
        self.args = string
