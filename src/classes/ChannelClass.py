from abc import abstractmethod


class Channel:

    @abstractmethod
    def readline(self) -> str:
        pass

    def writeline(self, string: str):
        pass


class StdChannel(Channel):
    def __init__(self):
        pass

    def readline(self) -> str:
        strline = input()
        return strline

    def writeline(self, string: str):
        print(string)


class PipeChannel(Channel):
    def __init__(self):
        self.args = None

    def readline(self):
        return self.args

    def writeline(self, string: str):
        self.args = string
