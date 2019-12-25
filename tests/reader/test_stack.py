from stream import IterStream

from clausewitz.reader.node import NodeReader
from clausewitz.reader.stack import ReaderStack

s = '''
a = { x y }
b >= 0
'''


def test():
    stream = IterStream(s)
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
