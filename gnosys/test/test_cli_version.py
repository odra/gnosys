from gnosys.cli import cli


def test_version(cli_runner):
    res = cli_runner.invoke(cli, ['version'])

    assert 0 == res.exit_code
    assert 'v0.1.0\n' == res.output
