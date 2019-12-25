import string
from functools import wraps

from logical.collection import In

from .stack import Push
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


class NameReader(AbstractWordReader):
    START = string.ascii_letters
    END = ~In(string.ascii_letters + string.digits)


class NumberReader(AbstractWordReader):
    START = string.digits
    END = ~In(string.digits)


class OperatorReader(AbstractWordReader):
    START = string.punctuation
    END = ~In(string.punctuation)
