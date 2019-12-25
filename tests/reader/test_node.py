import pytest

from clausewitz.reader.node import NodeReader
from clausewitz.reader.stack import Push
from clausewitz.reader.string import StringReader, CommentReader
from clausewitz.reader.word import WordReader


def test_push():
    reader = NodeReader()
    with pytest.raises(Push) as e_info:
        reader.read('"')
    assert isinstance(e_info.value.reader, StringReader)

    with pytest.raises(Push) as e_info:
        reader.read('#')
    assert isinstance(e_info.value.reader, CommentReader)

    with pytest.raises(Push) as e_info:
        reader.read('{')
    assert isinstance(e_info.value.reader, NodeReader)

    with pytest.raises(Push) as e_info:
        reader.read('a')
    assert isinstance(e_info.value.reader, WordReader)

    reader.read(' ')


def test_child():
    reader = NodeReader()
    try:
        reader.read('"')
    except Push as push:
        push.reader.read('a')
    reader.cleanup()
    assert reader.result == (
        ('a',),
    )
