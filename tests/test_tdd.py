from datetime import datetime, timedelta

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


def test_complete_all(test_data):
    all_complete = tasks.complete_all_tasks(test_data)

    assert all([task["completed"] for task in all_complete])


@pytest.mark.parametrize(
    "task_input,expected_output",
    [([], []), ([{}], [{"completed": True}])],
)
def test_complete_all_edge_cases(task_input, expected_output):
    """Tests sorting on specific edge cases.

    Args:
        task_input (list[dict[str, Any]]): The test data (given manually).
        expected_output (list[dict[str, Any]]): The expected output.
    """
    sorted_tasks = tasks.complete_all_tasks(task_input)

    assert sorted_tasks == expected_output


# ---------- TASK STATS ----------


def test_get_task_stats(test_data):
    stats = tasks.get_task_stats(test_data)  # (total, incomplete, complete, overdue)

    assert (
        stats[1] >= stats[3]
    ), "There cannot be more overdue tasks than there are incomplete tasks."
    assert stats == (4, 2, 2, 2)


_today = datetime.now().strftime(tasks.DATE_FORMAT)
_tomorrow = (datetime.now() + timedelta(days=1)).strftime(tasks.DATE_FORMAT)
_yesterday = (datetime.now() - timedelta(days=1)).strftime(tasks.DATE_FORMAT)


@pytest.mark.parametrize(
    "task_input,expected_output",
    [
        ([], (0, 0, 0, 0)),
        ([{}], (1, 1, 0, 0)),  # 1 incomplete because {} is not a completed task
        (
            [{"completed": True}, {"completed": True}, {"completed": False}],
            (3, 1, 2, 0),
        ),
        (
            [
                {"completed": True, "due_date": _yesterday},
                {"completed": True, "due_date": _tomorrow},
                {"completed": False, "due_date": _tomorrow},
                {"completed": False, "due_date": _today},
                {"completed": False, "due_date": _yesterday},
            ],
            (5, 3, 2, 1),
        ),
    ],
)
def test_get_task_stats_edge_cases(task_input, expected_output):
    """Tests sorting on specific edge cases.

    Args:
        task_input (list[dict[str, Any]]): The test data (given manually).
        expected_output (tuple[int, int, int, int]): The expected output.
    """
    sorted_tasks = tasks.get_task_stats(task_input)

    assert sorted_tasks == expected_output
