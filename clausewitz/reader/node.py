import string

from . import AbstractReader
from .abstract import AbstractMultiNodeReader
from .string import StringReader, CommentReader
from .word import WordReader


class NodeReader(AbstractMultiNodeReader):
    START = '{'
    END = '}'

    OPERATORS = ('=', '>', '>=', '<', '<=')

    DEFAULT_CHILDREN = (
        StringReader,
        CommentReader,
        'self',
        WordReader,
    )

    def __init__(self, end=None):
        super().__init__(end)
        self.__result = []
        self._current = []

    def _process_child_result(self, child: AbstractReader):
        if isinstance(child, CommentReader):
            return

        if child.result in self.OPERATORS:
            pass
        elif self._last in self.OPERATORS:
            pass
        else:
            self._push()

        self._add(child.result)

    def _read_self(self, c):
        if c not in string.whitespace:
            raise ValueError(f"Unsupported character: {c}")

    @property
    def _last(self):
        if not self._current:
            return None
        return self._current[-1]

    def _add(self, item):
        self._current.append(item)

    def _push(self):
        if self._current:
            self.__result.append(self._current)
        self._current = []

    def cleanup(self):
        super().cleanup()
        self._push()

    @property
    def result(self):
        return tuple([
            tuple(item)
            for item in self.__result
        ])
