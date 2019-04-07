import os

from setuptools import setup, find_packages

root_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_dir, "VERSION")) as f:
    VERSION = f.read().rstrip()

extra_test = [
    'pytest',
    'pytest-runner',
]
extra_dev = extra_test

extra_ci = extra_test

setup(
    name='pypdx-clausewitz',

    version=VERSION,

    python_requires='>=3.6',

    extras_require={
        'test': extra_test,
        'dev': extra_dev,

        'ci': extra_ci,
    },

    packages=find_packages(),

    url='https://github.com/PyPDX/clausewitz',

    license='PyPDX',

    author='PyPDX',
    author_email='pypdx@michaelkim0407.com',

    description='',
)
