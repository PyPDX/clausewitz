import pytest

from clausewitz.reader.stack import Pop
from clausewitz.reader.string import StringReader

s = 'hla4j9dlna'
quote = StringReader.END


def test():
    reader = StringReader()
    for c in s:
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


def test_escape():
    s_escape = 'fjoa3df\\"a3ae'
    reader = StringReader()
    for c in s_escape:
        reader.read(c)
    assert reader.result == s_escape
