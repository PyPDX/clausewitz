import string

from .abstract import AbstractNodeReader, Start, Match
from .stack import Push
from .string import AbstractStringReader

__author__ = 'Michael'


class AbstractWordReader(AbstractNodeReader):
    NOT_START = string.whitespace
    END = string.whitespace

    @classmethod
    def start(cls, not_start=None, *args, **kwargs):
        if not_start is None:
            not_start = cls.NOT_START
        not_start = Match(not_start)

        def read(c):
            if not_start(c):
                return
            reader = cls(*args, **kwargs)
            reader.read(c)
            raise Push(reader)

        return Start(cls, read)


class WordReader(AbstractWordReader, AbstractStringReader):
    pass
