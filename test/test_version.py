from re import match

from vecgl import __version__


def test_version():
    assert match("^([0-9]+\\.)+[a-z0-9+\\.]*$", __version__)
