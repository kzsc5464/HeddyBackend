"""Dummy test script for python-project-template."""

import pytest

from main import dummy


def test_dummy() -> None:
    """Test dummy numbers."""
    with pytest.raises(AssertionError):
        dummy()
    assert dummy(0) == 0
