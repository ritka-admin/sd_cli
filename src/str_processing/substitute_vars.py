import sys

sys.path.append("..")
from classes.ChannelClass import *
from classes.StringClass import *
from classes.ExceptionClass import *
from typing import List


def substitute_vars(arg: List[List[InterpretString | PlainString]], envs: dict) -> str:
    """
    Method to substitute variable if need
    Parameters:
    envs: dict of environment variables in system
    """
    new_raw_str = []
    for arg_list in arg:
        for elem in arg_list:
            if isinstance(elem, InterpretString) and elem.raw_str.find("$")>=0:
                new_int_str = []
                st = elem.raw_str.find("$")
                end = elem.raw_str.find("$", st + 1)
                size = len(elem.raw_str)
                new_int_str.append(elem.raw_str[:st])
                while st < size and st >= 0 and end < size and end >= 0:
                    try:
                        value = envs[elem.raw_str[st + 1 : end]]
                    except KeyError:
                        value = ""
                    st = end
                    end = elem.raw_str.find("$", st + 1)
                    new_int_str.append(value)
                if st < size - 1:
                    try:
                        value = envs[elem.raw_str[st + 1 : size]]
                    except KeyError:
                        value = ""
                    new_int_str.append(value)
                else:
                    new_int_str.append("$")

                new_raw_str.append("".join(new_int_str))
            else:
                new_raw_str.append(elem.raw_str)

    return " ".join(new_raw_str)
