import pytest

from src import tasks
from tests.common import TEST_DATA


@pytest.fixture
def test_data():
    return [task.copy() for task in TEST_DATA]


# ---------- SORTING ----------


@pytest.mark.parametrize(
    "sort_by,asc,expected_order",
    [
        ("id", True, range(len(TEST_DATA))),  # already sorted in this order
        ("id", False, reversed(range(len(TEST_DATA)))),
        ("due_date", True, [2, 0, 3, 1]),
        ("due_date", False, [1, 3, 0, 2]),
    ],
)
def test_sort_on_test_data(test_data, sort_by, asc, expected_order):
    """Tests sorting on complete test data.

    Args:
        test_data (list[dict[str, Any]]): The test data (given by fixture).
        sort_by (str): The property to sort by.
        asc (bool): True to sort ascending, False otherwise.
        expected_order (Iterable[int]): The indices of TEST_DATA in the expected order.
    """
    sorted_tasks = tasks.sort_tasks(test_data, sort_by, asc)

    assert sorted_tasks == [test_data[i] for i in expected_order]


@pytest.mark.parametrize(
    "task_input,sort_by,asc,expected_output",
    [
        ([], "id", True, []),
        ([{"foo": 1, "bar": "baz"}], "id", True, [{"foo": 1, "bar": "baz"}]),
        (
            [
                {"foo": 2, "bar": "baz"},
                *[dict(id=i) for i in reversed(range(10))],
                {"foo": 1, "bar": "baz"},
            ],
            "id",
            True,
            [
                *[dict(id=i) for i in range(10)],
                {"foo": 2, "bar": "baz"},
                {"foo": 1, "bar": "baz"},
            ],
        ),
    ],
)
def test_sort_edge_cases(task_input, sort_by, asc, expected_output):
    """Tests sorting on specific edge cases.

    Args:
        task_input (list[dict[str, Any]]): The test data (given manually).
        sort_by (str): The property to sort by.
        expected_output (list[dict[str, Any]]): The expected output.
    """
    sorted_tasks = tasks.sort_tasks(task_input, sort_by, asc)

    assert sorted_tasks == expected_output


# ---------- COMPLETE ALL ----------


# ---------- Other Thing ----------
