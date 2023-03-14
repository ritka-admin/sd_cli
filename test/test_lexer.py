import pytest
from src.str_processing.lexer import lexer
from src.classes.StringClass import InterpretString, PlainString


def test_quotes():
    raw_cmd = ("echo $HOME")
    lexer_res = lexer(raw_cmd)
    command, = lexer_res
    assert len(lexer_res) == 1      # list of the one command tokens
    assert isinstance(command[0], InterpretString)
    assert isinstance(command[1], InterpretString)
