import os
import pytest
from src.classes.CommandClass import *
from src.classes.ChannelClass import StdChannel
from src.str_processing.lexer import lexer
from src.str_processing.parser import parser
from src.str_processing.substitute_vars import substitute_vars


envs = dict(os.environ.items())
InCh = StdChannel()
OutCh = StdChannel()


@pytest.fixture()
def lex_and_pars_without_grep(request) -> Command:
    lexer_res = lexer(request.param)
    subst = lexer(substitute_vars(lexer_res, envs))
    pars_res = parser(subst[0])
    return pars_res


@pytest.mark.parametrize('lex_and_pars_without_grep', ["echo sdsdas"], indirect=True)
def test_echo_command(lex_and_pars_without_grep):
    res = lex_and_pars_without_grep
    assert isinstance(res, EchoCommand)
