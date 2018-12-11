from clausewitz.reader.node import NodeReader
from clausewitz.reader.stack import ReaderStack
from clausewitz.reader.stream import Stream

__author__ = 'Michael'

s = '''
a = { x y }
b >= 0
'''


def test():
    stream = Stream(s)
    reader = NodeReader()
    stack = ReaderStack(stream, reader)
    stack.read_all()
    assert stack.result == (
        ('a', '=', (
            ('x',),
            ('y',),
        )),
        ('b', '>=', '0'),
    )
