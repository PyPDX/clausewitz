from clausewitz.reader.node import NodeReader
from clausewitz.reader.stack import ReaderStack

s = '''
a = { x y }
b>= 0
c =1
d=2.1
'''


def test():
    reader = NodeReader()
    stack = ReaderStack(s, reader)
    stack.read_all()
    assert stack.result == (
        ('a', '=', (
            ('x',),
            ('y',),
        )),
        ('b', '>=', 0),
        ('c', '=', 1),
        ('d', '=', 2.1),
    )
