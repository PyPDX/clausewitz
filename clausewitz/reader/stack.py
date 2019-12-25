from typing import List

from . import AbstractReader


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
    def __init__(self, popped=''):
        self.popped = popped


class ReaderStack(object):
    def __init__(self, stream, reader: AbstractReader):
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

    def __read_one(self, c):
        try:
            self.__reader.read(c)
        except Push as push:
            self.__push(push.reader)
        except Pop as pop:
            self.__pop()
            for c in pop.popped:
                self.__read_one(c)

    def read_all(self):
        for c in self.stream:
            self.__read_one(c)

        if len(self.__readers) > 1:
            raise UnfinishedStream

        self.__reader.cleanup()

    @property
    def result(self):
        return self.__reader.result
