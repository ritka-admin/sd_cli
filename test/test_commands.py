import os
import io
import pytest
import tempfile
import subprocess
from src.classes.CommandClass import *
from src.str_processing.lexer import lexer
from src.str_processing.parser import parser
from src.str_processing.substitute_vars import substitute_vars


file = tempfile.NamedTemporaryFile(mode='r+')
envs = dict(os.environ.items())
InCh = StdChannel()
OutCh = StdChannel()


@pytest.fixture(scope='function')
def lex_and_pars_without_grep(request) -> Command:
    lexer_res = lexer(request.param)
    subst = lexer(substitute_vars(lexer_res, envs))
    pars_res = parser(subst[0])
    return pars_res


@pytest.mark.parametrize('lex_and_pars_without_grep, arg',
                         [("echo sdsdas", 'sdsdas'),
                          ("echo 'dssdfasd'", 'dssdfasd'),
                          ("echo \"qwerty\"", "qwerty"),
                          ("echo \"$HOME\"", envs['HOME']),
                          ("echo '$USER'", '$USER'),
                          ('echo "\n\n\n\n\t$HOME"', envs['HOME'])],
                         indirect=["lex_and_pars_without_grep"])
def test_echo_command(lex_and_pars_without_grep, arg):
    command = lex_and_pars_without_grep
    assert isinstance(command, EchoCommand)
    with io.StringIO() as sys.stdout:
        command.execute(InCh, OutCh)
        res = sys.stdout.getvalue()
    assert res.rstrip() == arg


@pytest.mark.parametrize('lex_and_pars_without_grep', ['exit'], indirect=True)
def test_exit_command(lex_and_pars_without_grep):
    obj = lex_and_pars_without_grep
    assert isinstance(obj, ExitCommand)
    try:
        obj.execute(InCh, OutCh)
    except SpecialExitException:
        assert True
    except Exception:
        assert False


@pytest.mark.parametrize('lex_and_pars_without_grep, arg',
                         [("pwd", ''), ("pwd", "1235")],
                         indirect=['lex_and_pars_without_grep'])
def test_pwd_command(lex_and_pars_without_grep, arg):
    command = lex_and_pars_without_grep
    assert isinstance(command, PwdCommand)
    with io.StringIO() as sys.stdout:
        command.execute(InCh, OutCh)
        res = sys.stdout.getvalue()
    status = subprocess.getstatusoutput(' '.join(['pwd', arg]))
    assert status[0] == 0               # exit code is 0
    assert res.rstrip() == status[1]    # output is the same


@pytest.mark.parametrize('lex_and_pars_without_grep, arg, valid',
                         [("cat 'qwerty'", 'qwerty', False)],
                          # (f"cat {file.name}", "qwerty", True),
                         indirect=['lex_and_pars_without_grep'])
def test_cat_command(lex_and_pars_without_grep, arg, valid):
    command = lex_and_pars_without_grep
    assert isinstance(command, CatCommand)
    file.write(arg)
    with io.StringIO() as sys.stdout:
        in_file = file.read()
        command.execute(InCh, OutCh)
        res = sys.stdout.getvalue()
    if valid:
        status = subprocess.getstatusoutput(f"cat {file.name}")
        assert status[0] == 0             # exit code is 0
        assert res.rstrip() == in_file    # output is the same
    else:
        status = subprocess.getstatusoutput(f"cat {arg}")
        assert status[0] != 0


def test_wc_command():
    pass


def test_external_command():
    pass

