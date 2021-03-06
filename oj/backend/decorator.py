import configparser
import inspect
from typing import Tuple, List, Dict, Any
from .core import Problem

CONFIG = configparser.ConfigParser()
CONFIG.read("oj.ini")


def special_judge(func):
    """Customize judge function

    Notice:
        func(self, expected, answer) -> bool
    """

    def _judge_wrapper(self, expected, answer) -> bool:
        return func(self, expected, answer)
    return _judge_wrapper


def special_data_generator(func):
    """Customize data generator

    Notice:
        yields (args, kwargs, ret) which args, kwargs are input parameters and ret is output
    """

    def _data_generator_wrapper(self) -> Tuple[List, Dict, Any]:
        return func(self)
    return _data_generator_wrapper


def problem(cls):
    """Append test feature

    Notice:
        Configure data path with [oj.ini]-[data]-[root]
    """
    # pylint: disable=W0223
    class ProblemWrapper(cls, Problem):
        __test__ = True
        __data__ = CONFIG["data"]["root"]
        __title__ = cls.__name__

    for _, func in inspect.getmembers(cls, predicate=inspect.isfunction):
        if func.__name__ == "_judge_wrapper":
            ProblemWrapper.judge = func
        elif func.__name__ == "_data_generator_wrapper":
            ProblemWrapper.generate_cases = func

    return ProblemWrapper
