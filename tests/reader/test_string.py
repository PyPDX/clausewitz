import pytest
from stream import IterStream

from clausewitz.reader.stack import Pop
from clausewitz.reader.string import StringReader

s = 'hla4j9dlna'
quote = StringReader.END


def test():
    stream = IterStream(s)
    reader = StringReader()
    for c in stream:
        reader.read(c)
    assert reader.result == s


def test_pop():
    assert quote == '"'

    with pytest.raises(Pop):
        StringReader().read(quote)


def test_end():
    quote2 = '/'
    reader = StringReader(end=quote2)

    reader.read(quote)
    assert reader.result == quote

    with pytest.raises(Pop):
        reader.read(quote2)
