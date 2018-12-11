from typing import Type, List

from . import AbstractReader
from .stack import Push, Pop

__author__ = 'Michael'


class Match(object):
    def __init__(self, match):
        if match is None:
            raise ValueError('cannot be None')
        self.match = match

    def __call__(self, val):
        return val in self.match


class Start(object):
    def __init__(self, cls, func):
        self.cls = cls
        self.func = func

    def __call__(self, val):
        self.func(val)


class AbstractNodeReader(AbstractReader):
    START = None
    END = None

    def __init__(self, end=None):
        if end is None:
            end = self.END
        self.end = Match(end)

    def read(self, c):
        if self.end(c):
            self.cleanup()
            raise Pop
        self._read(c)

    def _read(self, c):
        raise NotImplementedError

    @classmethod
    def start(cls, start=None, *args, **kwargs):
        if start is None:
            start = cls.START
        start = Match(start)

        def read(c):
            if start(c):
                raise Push(cls(*args, **kwargs))

        return Start(cls, read)


class AbstractMultiNodeReader(AbstractNodeReader):
    DEFAULT_CHILDREN = ()

    def __init__(self, end=None):
        super().__init__(end)
        self.__children: List[Start] = list(self.DEFAULT_CHILDREN)
        self.__child = None

    def register(self, cls: Type[AbstractNodeReader], *args, **kwargs):
        for child in self.__children:
            if child.cls == cls:
                raise ValueError('Already registered')
        self.__children.append(cls.start(*args, **kwargs))

    def unregister(self, cls: Type[AbstractNodeReader]):
        self.__children: List[Start] = [
            child
            for child in self.__children
            if child.cls != cls
        ]

    def _process_child_result(self, child: AbstractReader):
        raise NotImplementedError

    def __process_child(self):
        if self.__child is not None:
            self._process_child_result(self.__child)
            self.__child = None

    def _read(self, c):
        self.__process_child()

        for child in self.__children:
            try:
                child(c)
            except Push as push:
                self.__child = push.reader
                raise

        self._read_self(c)

    def cleanup(self):
        self.__process_child()

    def _read_self(self, c):
        raise NotImplementedError
