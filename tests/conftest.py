import pytest


@pytest.fixture
def sample():
    return open('tests/data/sample.txt', 'rb').readline
