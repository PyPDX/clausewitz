import pytest

from clausewitz.reader.stack import Pop
from clausewitz.reader.word import WordReader

s = 'jaoej490a anvmla'


def test():
    stream = iter(s)
    reader = WordReader()
    with pytest.raises(Pop):
        for c in stream:
            reader.read(c)
    assert reader.result == s.split()[0]

    reader2 = WordReader()
    for c in stream:
        reader2.read(c)
    assert reader2.result == s.split()[1]
