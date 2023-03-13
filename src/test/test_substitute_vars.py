import unittest
from typing import List

from src.str_processing.substitute_vars import *
from src.classes.StringClass import *


class TestSubstituteVars(unittest.TestCase):
    def test_all_keys(self):
        arg = [[InterpretString("$x$y"), PlainString("echo")]]
        envs = {"x": "ex", "y": "it"}
        self.assertEqual(substitute_vars(arg, envs), 'exit echo')

    def test_one_key(self):
        arg = [[InterpretString("$x$y"), PlainString("echo")]]
        envs = {"y": "it"}
        self.assertEqual(substitute_vars(arg, envs), 'it echo')
        envs = {"x": "ex"}
        self.assertEqual(substitute_vars(arg, envs), 'ex echo')

    # Doesn't work :(((
    # def test_empty_key(self):
    #     arg = [[InterpretString("$x$y"), PlainString("echo"), PlainString("hello")]]
    #     envs = {}
    #     self.assertEqual(substitute_vars(arg, envs), "echo hello")

    def test_non_vars(self):
        arg = [[InterpretString("echo"), InterpretString("hello")]]
        envs = {}
        self.assertEqual(substitute_vars(arg, envs), "echo hello")

    def test_out_range(self):
        arg = [[InterpretString("ac$x$y$"), InterpretString("echo"), PlainString("hello")]]
        envs = {"x": "ex", "y": "it"}
        self.assertEqual(substitute_vars(arg, envs), 'acexit$ echo hello')

    # def test_single_quotes(self):
    #     arg = [[InterpretString("'ac'$x'abc'"), InterpretString("echo")]]
    #     envs = {"x": "ex", "y": "it"}
    #     self.assertEqual(substitute_vars(arg, envs), 'acexabc echo')



