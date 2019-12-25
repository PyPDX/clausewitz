import string
from functools import wraps

from logical.collection import In

from .stack import Push
from .string import AbstractStringReader

__author__ = 'Michael'


class WordReader(AbstractStringReader):
    START = ~In(string.whitespace)
    END = string.whitespace

    @classmethod
    def start(cls, start=None, *args, **kwargs):
        read = super().start(start, *args, **kwargs)

        @wraps(read)
        def new_read(c):
            try:
                read(c)
            except Push as push:
                push.reader.read(c)
                raise

        return new_read
