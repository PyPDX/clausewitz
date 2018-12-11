from typing import List

from . import AbstractReader
from .stream import Stream

__author__ = 'Michael'


class InvalidStream(Exception):
    pass


class LeftoverStream(InvalidStream):
    """
    Stream is not finished yet after the starting reader is popped.
    """
    pass


class UnfinishedStream(InvalidStream):
    """
    Stream ended without wrapping up readers.
    """
    pass


class Push(Exception):
    def __init__(self, reader: AbstractReader):
        self.reader = reader


class Pop(Exception):
    pass


class ReaderStack(object):
    def __init__(self, stream: Stream, reader: AbstractReader):
        self.stream = stream
        self.__readers: List[AbstractReader] = [reader]

    def __push(self, reader: AbstractReader):
        self.__readers.append(reader)

    def __pop(self):
        self.__readers.pop(-1)

    @property
    def __reader(self) -> AbstractReader:
        try:
            return self.__readers[-1]
        except IndexError:
            raise LeftoverStream from None

    def read_all(self):
        for c in self.stream:
            try:
                self.__reader.read(c)
            except Push as push:
                self.__push(push.reader)
            except Pop:
                self.__pop()

        if len(self.__readers) > 1:
            raise UnfinishedStream

        self.__reader.cleanup()

    @property
    def result(self):
        return self.__reader.result
