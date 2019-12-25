import pytest

from clausewitz.reader.stack import Pop
from clausewitz.reader.word import NameReader

s = 'jaoej490a anvmla'


def test():
    stream = iter(s)
    reader = NameReader()
    with pytest.raises(Pop):
        for c in stream:
            reader.read(c)
    assert reader.result == s.split()[0]

    reader2 = NameReader()
    for c in stream:
        reader2.read(c)
    assert reader2.result == s.split()[1]
