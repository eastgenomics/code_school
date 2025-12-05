import pandas as pd
import pytest

from .. import assign_santa as assign


def test_convert_excluded_dataframe_to_dict():
    """
    Test when given a dataframe of excluded pairs, this is converted
    properly to a dictionary
    """
    names = ["Alice", "Bob", "Charlie", "Erin"]
    excluded = pd.DataFrame(
        {
            "giver": ["Alice", "Alice", "Bob"],
            "receiver": ["Bob", "Charlie", "Erin"],
        }
    )
    expected = {"Alice": ["Bob", "Charlie"], "Bob": ["Erin"]}
    result = assign.convert_excluded_dataframe_to_dict(excluded, names)

    assert result == expected


def test_error_raised_if_less_than_2_names():
    """
    Test error raised if <2 names given as input
    """
    names = ["Alice"]
    with pytest.raises(ValueError):
        assign.validate_participants(names)


def test_assign_secret_santa_simple():
    """
    Test names assigned correctly with simple case
    """
    names = ["Alice", "Bob", "Charlie"]
    exclusions = {"Alice": ["Bob"]}
    result = assign.assign_secret_santa(names, exclusions, max_attempts=100)

    assert result == {"Alice": "Charlie", "Bob": "Alice", "Charlie": "Bob"}


def test_assign_secret_santa_impossible():
    """
    Test assign fails when it's impossible because the only participants can't
    have each other
    """
    names = ["Alice", "Bob"]
    exclusions = {"Alice": ["Bob"], "Bob": ["Alice"]}
    with pytest.raises(RuntimeError):
        assign.assign_secret_santa(names, exclusions, max_attempts=2)
