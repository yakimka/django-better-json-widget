import pytest

from better_json_widget import example


@pytest.mark.parametrize(
    "first,second,expected",
    [
        (1, 2, 3),
        (2, 4, 6),
        (-2, -3, -5),
        (-5, 5, 0),
    ],
)
def test_some_function(first, second, expected):
    """Example test with parametrization."""
    result = example.some_function(first, second)

    assert result == expected
