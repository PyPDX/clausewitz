import string
from functools import wraps

from logical.collection import In

from .stack import Push, Pop
from .string import AbstractStringReader


class AbstractWordReader(AbstractStringReader):
    @classmethod
    def start(cls, start=None, *args, **kwargs):
        read = super().start(start, *args, **kwargs)

        @wraps(read)
        def new_read(c):
            try:
                read(c)
            except Push as push:
                push.reader.read(c)  # include the first character in result
                raise

        return new_read

    def read(self, c):
        try:
            super().read(c)
        except Pop as pop:
            pop.popped = c  # send the character back
            raise


class NameReader(AbstractWordReader):
    START = string.ascii_letters + '_'
    END = ~In(string.ascii_letters + string.digits + '_')


class NumberReader(AbstractWordReader):
    START = string.digits
    END = ~In(string.digits + '.')

    @property
    def result(self):
        result = super().result
        if '.' in result:
            return float(result)
        else:
            return int(result)


class OperatorReader(AbstractWordReader):
    _CHARACTERS = string.punctuation.replace('"', '').replace('_', '').replace('{', '')
    START = _CHARACTERS
    END = ~In(_CHARACTERS)
