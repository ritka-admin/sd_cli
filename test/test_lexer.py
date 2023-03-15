import pytest
from src.str_processing.lexer import lexer
from src.classes.StringClass import InterpretString, PlainString


def test_without_quotes():
    raw_cmd1 = ("echo $HOME")
    raw_cmd2 = ("echo fsdfsdfds'sdfsdfdsf")
    raw_cmd3 = ('echo dsdsad"sdfsdf"sdf')
    command1, = lexer(raw_cmd1)
    command2, = lexer(raw_cmd2)
    command3, = lexer(raw_cmd3)
    assert isinstance(command1[0], InterpretString)
    assert isinstance(command1[1], InterpretString)
    assert command2[1].raw_str == "fsdfsdfds'sdfsdfdsf"
    assert command3[1].raw_str == 'dsdsad"sdfsdf"sdf'
