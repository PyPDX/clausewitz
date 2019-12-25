import typing

from cached_property import cached_property
from logical.collection import In

from . import AbstractReader
from .stack import Push, Pop


class AbstractNodeReader(AbstractReader):
    START = None
    END = None

    def __init__(
            self,
            *,
            end=None,
    ):
        self.__end = end

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
        if not callable(start):
            start = In(start)

        def read(c):
            if start(c):
                raise Push(cls(*args, **kwargs))

        return read

    @cached_property
    def _end(self):
        end = self.__end
        if end is None:
            end = self.END
        if not callable(end):
            end = In(end)
        return end

    def end(self, c):
        return self._end(c)


class AbstractMultiNodeReader(AbstractNodeReader):
    DEFAULT_CHILDREN = ()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__children: typing.Dict[
            typing.Type[AbstractNodeReader],
            typing.Callable,
        ] = {}
        self._load_default()
        self.__child = None

    def _load_default(self):
        for child in self.DEFAULT_CHILDREN:
            if not isinstance(child, tuple):
                child = (child,)

            cls = child[0]
            if cls == 'self':
                cls = self.__class__

            if len(child) > 1:
                args = child[1]
            else:
                args = ()

            if len(child) > 2:
                kwargs = child[2]
            else:
                kwargs = {}

            self.register(cls, *args, **kwargs)

    def register(self, cls: typing.Type[AbstractNodeReader], *args, **kwargs):
        if cls in self.__children:
            raise ValueError('Already registered')
        self.__children[cls] = cls.start(*args, **kwargs)

    def unregister(self, cls: typing.Type[AbstractNodeReader]):
        del self.__children[cls]

    def _process_child_result(self, child: AbstractReader):
        raise NotImplementedError

    def __process_child(self):
        if self.__child is not None:
            self._process_child_result(self.__child)
            self.__child = None

    def _read(self, c):
        self.__process_child()

        for child in self.__children.values():
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
