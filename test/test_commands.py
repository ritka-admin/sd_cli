import os
import io
import pytest
import tempfile
import subprocess
from src.classes.CommandClass import *
from src.str_processing.lexer import lexer
from src.str_processing.parser import parser
from src.str_processing.substitute_vars import substitute_vars


file = tempfile.NamedTemporaryFile(mode='r+', dir='/tmp')
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
                         [("cat 'qwerty'", 'qwerty', False),
                          (f"cat {file.name}", "qwerty", True),
                          (f"cat {file.name}", "\'1234234\' gdfgsfsdf", True)],
                         indirect=['lex_and_pars_without_grep'])
def test_cat_command(lex_and_pars_without_grep, arg, valid):
    command = lex_and_pars_without_grep
    assert isinstance(command, CatCommand)
    sys_file = tempfile.NamedTemporaryFile(mode='r+')
    sys_file.write(arg)
    with io.StringIO() as sys.stdout:
        in_file = sys_file.read()
        command.execute(InCh, OutCh)
        res = sys.stdout.getvalue()
    if valid:
        status = subprocess.getstatusoutput(f"cat {sys_file.name}")
        assert status[0] == 0             # exit code is 0
        assert res.rstrip() == in_file    # output is the same
    else:
        status = subprocess.getstatusoutput(f"cat {arg}")
        assert status[0] != 0


@pytest.mark.parametrize('lex_and_pars_without_grep, arg, valid',
                         [("wc 'qwerty'", 'qwerty', False),
                          (f"wc {file.name}", "qwerty", True),
                          (f"wc {file.name}", "\'1234234\' gdfgsfsdf", True)],
                         indirect=['lex_and_pars_without_grep'])
def test_wc_command(lex_and_pars_without_grep, arg, valid):
    command = lex_and_pars_without_grep
    assert isinstance(command, WcCommand)
    file.write(arg)
    with io.StringIO() as sys.stdout:
        command.execute(InCh, OutCh)
        res = sys.stdout.getvalue()
    if valid:
        status = subprocess.getstatusoutput(f"wc {file.name}")
        assert status[0] == 0               # exit code is 0
        assert res.rstrip() == status[1]    # output is the same
    else:
        status = subprocess.getstatusoutput(f"wc {arg}")
        assert status[0] != 0


def test_external_command():
    pass

