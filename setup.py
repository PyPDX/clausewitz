import os

from setuptools import setup

root_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_dir, "VERSION")) as f:
    VERSION = f.read().rstrip()

setup(
    name='pypdx-clausewitz',

    version=VERSION,

    python_requires='>=3.6',

    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "pytest",
    ],

    packages=['clausewitz'],

    url='https://github.com/PyPDX/clausewitz',

    license='PyPDX',

    author='PyPDX',
    author_email='pypdx@michaelkim0407.com',

    description='',
)
