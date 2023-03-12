from abc import abstractmethod


class Channel:
    """
    Abstract class for reading and writing
    """

    @abstractmethod
    def readline(self) -> str:
        pass

    def writeline(self, string: str) -> None:
        pass


class StdChannel(Channel):
    """
    Class for reading and writing from(to) stdin, stdout.
    """

    def __init__(self):
        pass

    def readline(self) -> str:
        """
        Method for reading from stdin.

        Returns:
            String that was readed
        """
        strline = input()
        return strline

    def writeline(self, string: str) -> None:
        """
        Method for writing to stdout.
        Parameters:
            string: string to write to stdout.
        """
        print(string)


class PipeChannel(Channel):
    """
    Class for reading and writing from(to) output(input) of other command
    """

    def __init__(self):
        self.args = None

    def readline(self):
        """
        Method for reading from stdin of other command.

        Returns:
            String that was readed
        """
        return self.args

    def writeline(self, string: str) -> None:
        """
        Method for writing to input of another command.

        Parameters:
            string: string to input of another command.
        """
        self.args = string
