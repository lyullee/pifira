"""Release metadata consistency tests."""

import pytest

from tools.check_release_version import check_release_version, declared_versions


def test_release_metadata_versions_match():
    assert set(declared_versions().values()) == {"0.3.0"}
    assert check_release_version() == "0.3.0"
    assert check_release_version("v0.3.0") == "0.3.0"


def test_release_tag_mismatch_is_rejected():
    with pytest.raises(RuntimeError, match="does not match"):
        check_release_version("v0.2.0")
