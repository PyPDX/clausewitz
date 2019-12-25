from setuptools import setup, find_packages

from clausewitz import __version__

requirements = [
    'cached-property',
    'logical-func',
]

extra_test = [
    'pytest>=4',
    'pytest-runner>=4',
    'pytest-cov>=2',
]
extra_dev = extra_test

extra_ci = extra_test + [
    'python-coveralls',
]

setup(
    name='pypdx-clausewitz',

    version=__version__,

    python_requires='>=3.6',

    install_requires=requirements,

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
