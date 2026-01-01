import os
import pytest


@pytest.fixture
def testdir():
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def fixdir(testdir):
    return f'{testdir}/fixtures'


@pytest.fixture
def cfg():
    return {
        'data': {
            'sources': [
                'file:///my/data/file.txt',
                    'http://my-url/file.txt'
            ]
        }
    }
