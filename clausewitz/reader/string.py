from .abstract import AbstractNodeReader

__author__ = 'Michael'


class AbstractStringReader(AbstractNodeReader):
    def __init__(self, end=None):
        super().__init__(end)
        self._result = ''

    def _read(self, c):
        self._result += c

    @property
    def result(self):
        return self._result


class StringReader(AbstractStringReader):
    START = '"'
    END = '"'


class CommentReader(AbstractStringReader):
    START = '#'
    END = '\n'
