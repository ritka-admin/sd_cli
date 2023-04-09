import pytest

import os
import platform
from pathlib import Path

from src.classes.ChannelClass import Channel, StdChannel
from src.classes.CommandClass import CdCommand
from src.classes.ExceptionClass import InputError
from src.classes.StringClass import PlainString


def test_cd_no_args():
    cmd = CdCommand([])
    cmd.execute(Channel(), Channel())
    assert os.getcwd() == os.environ['USERPROFILE'] if platform.system() == "Windows" else os.environ['USERPROFILE']


def test_cd_with_existing_directory():
    current_dir = os.getcwd()
    new_dir = os.path.join(current_dir, 'test_dir')
    os.mkdir(new_dir)
    cmd = CdCommand([PlainString('test_dir')])
    cmd.execute(Channel(), Channel())
    assert os.getcwd() == new_dir
    os.chdir(current_dir)
    os.rmdir(new_dir)


def test_cd_with_nonexistent_directory():
    cmd = CdCommand([PlainString('nonexistent_dir')])
    nonexistent_path = Path(os.getcwd()) / Path('nonexistent_dir')
    try:
        cmd.execute(StdChannel(), StdChannel())
    except InputError as e:
        assert str(e) == f"cd: {nonexistent_path}: No such file or directory"
