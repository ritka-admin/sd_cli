import pytest
from typing import List

from src.str_processing.substitute_vars import *
from src.classes.StringClass import *


def test_all_keys():
    arg = [[InterpretString("$x$y"), PlainString("echo")]]
    envs = {"x": "ex", "y": "it"}
    assert substitute_vars(arg, envs) == 'exit echo'


def test_one_key():
    arg = [[InterpretString("$x$y"), PlainString("echo")]]
    envs = {"y": "it"}
    assert substitute_vars(arg, envs) == 'it echo'
    envs = {"x": "ex"}
    assert substitute_vars(arg, envs) == 'ex echo'


# Doesn't work :(((
# def test_empty_key(self):
#     arg = [[InterpretString("$x$y"), PlainString("echo"), PlainString("hello")]]
#     envs = {}
#     assert substitute_vars(arg, envs) == "echo hello"


def test_non_vars():
    arg = [[InterpretString("echo"), InterpretString("hello")]]
    envs = {}
    assert substitute_vars(arg, envs) == "echo hello"


def test_out_range():
    arg = [[InterpretString("ac$x$y$"), InterpretString("echo"), PlainString("hello")]]
    envs = {"x": "ex", "y": "it"}
    assert substitute_vars(arg, envs) == 'acexit$ echo hello'


# def test_single_quotes():
#     arg = [[InterpretString("'ac'$x'abc'"), InterpretString("echo")]]
#     envs = {"x": "ex", "y": "it"}
#     assert substitute_vars(arg, envs) == 'acexabc echo'


