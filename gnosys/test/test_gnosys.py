# SPDX-License-Identifier: AGPL-3.0-only
# test top level module
# Copyright (C) 2026 Leonardo Rossetti

from gnosys import __version__


def test_version():
    assert '0.0.1' == __version__
