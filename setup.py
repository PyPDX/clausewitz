from setuptools import setup, find_packages

from clausewitz import __version__

requirements = [
    'cached-property',
    'returns-decorator',
]

extra_test = [
    'flake8',
    'flake8-commas',
    'flake8-print',
    'flake8-quotes',

    'pytest>=4',
    'pytest-runner>=4',
    'pytest-cov>=2',
]
extra_dev = extra_test

extra_ci = extra_test + [
    'coverage==4.*',
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

    entry_points={
        'console_scripts': [
            'tokenize-prepare=clausewitz.util.tokenize:prepare_cmd',
            'pdx-jsonify=clausewitz.parse:parse_cmd',
        ],
    },

    url='https://github.com/PyPDX/clausewitz',

    license='PyPDX',

    author='PyPDX',
    author_email='pypdx@michaelkim0407.com',

    description='',
)
