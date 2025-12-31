import pathlib

import pytest

from gnosys.config import Config


def test_load_yaml_ok(fixdir):
    c = Config.from_path(pathlib.Path(f'{fixdir}/config.yml'))
    data = {'gnosys': {}}

    assert Config(data) == c


def test_load_yaml_error_filepath(fixdir):
    with pytest.raises(FileNotFoundError):
        Config.from_path(pathlib.Path(f'{fixdir}/config.ym'))


def test_load_yaml_error_format(fixdir):
    with pytest.raises(AssertionError):
        Config.from_path(pathlib.Path(f'{fixdir}/config.invalid.yml'))
