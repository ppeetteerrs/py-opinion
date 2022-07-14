import pytest

import opinion
from opinion.midict import MIDict


@pytest.fixture
def version():
    return opinion.__version__


def test_version(version: str):
    assert version is not None


@pytest.fixture
def data():
    # Duplicate key test
    return MIDict(
        {
            ("a", "b"): "ak",
            ("a", "c"): "ac",
            ("a", "d"): "ad",
            ("a", "e"): "ae",
            ("a", "f"): "af",
            ("b", "b"): "bb",
            ("b", "a"): "ba",
            ("a", "b"): "ab",
        }
    )


def test_data(data: MIDict[str, str, str]):
    # Single item match
    assert data["a", "b"] == "ab"

    # Single level match
    assert data["a"] == {"b": "ab", "c": "ac", "d": "ad", "e": "ae", "f": "af"}

    # Single level preserve match
    assert data[["a"]] == {
        ("a", "b"): "ab",
        ("a", "c"): "ac",
        ("a", "d"): "ad",
        ("a", "e"): "ae",
        ("a", "f"): "af",
    }

    # Single level slice match
    assert data[["a"], :] == {
        ("a", "b"): "ab",
        ("a", "c"): "ac",
        ("a", "d"): "ad",
        ("a", "e"): "ae",
        ("a", "f"): "af",
    }

    # Single slice match
    assert data[:, "a":"b"] == {
        ("a", "b"): "ab",
        ("b", "a"): "ba",
        ("b", "b"): "bb",
    }

    # Set item test
    data["a", :] = "z"
    assert data[:] == {
        ("a", "b"): "z",
        ("a", "c"): "z",
        ("a", "d"): "z",
        ("a", "e"): "z",
        ("a", "f"): "z",
        ("b", "a"): "ba",
        ("b", "b"): "bb",
    }

    # Del item test
    del data["a", :]
    assert data[:] == {
        ("b", "a"): "ba",
        ("b", "b"): "bb",
    }
