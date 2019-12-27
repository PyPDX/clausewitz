import os
from contextlib import contextmanager

import pytest


@pytest.fixture
def data():
    @contextmanager
    def func(filename):
        with open(os.path.join('tests', 'data', filename), 'rb') as f:
            yield f.readline

    return func
