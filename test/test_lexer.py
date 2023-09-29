import pytest
from src.str_processing.lexer import lexer
from src.classes.StringClass import InterpretString, PlainString

# validation of the input string is preformed at parser level,
# so lexer just have to interpret the string with accordance
# with the quotes or its absence


@pytest.mark.parametrize("raw_cmd, arg", [("echo", "$HOME"),
                                          ("echo", "fsdfsdfds'sdfsdfdsf"),
                                          ("cat",  "dsdsad\"sdfsdf\"sdf")])
def test_without_quotes(raw_cmd, arg):
    raw_cmd = " ".join([raw_cmd, arg])
    command, = lexer(raw_cmd)
    assert isinstance(command[0], InterpretString)
    assert isinstance(command[1], InterpretString)
    assert command[1].raw_str == arg


@pytest.mark.parametrize("raw_cmd, arg", [("asfdasdf", 'sdfasdfsdf'),
                                          ("echo", '$HOME'),
                                          ("wc", 'sdfdfsf\"sdfdfsd')])
def test_with_unary_quotes(raw_cmd, arg):
    raw_cmd = f"{raw_cmd} '{arg}'"
    command, = lexer(raw_cmd)
    assert isinstance(command[0], InterpretString)
    assert isinstance(command[1], PlainString)
    assert command[1].raw_str == arg


@pytest.mark.parametrize("raw_cmd", [("pwd"), ("pinta"), ("exit")])
def test_one_word_with_binary_quotes(raw_cmd):
    command, = lexer(raw_cmd)
    assert isinstance(command[0], InterpretString)


@pytest.mark.parametrize("raw_cmd, arg", [("echo", "$HOME"),
                                          ("cat", "sdfdfdsf\'fsdfdsfsd")])
def test_two_words_with_binary_quotes(raw_cmd, arg):
    raw_cmd = f"{raw_cmd} \"{arg}\""
    command, = lexer(raw_cmd)
    assert isinstance(command[0], InterpretString)
    assert isinstance(command[1], InterpretString)
    assert command[1].raw_str == arg
