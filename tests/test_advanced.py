import pytest

from src import tasks
from tests.common import TEST_DATA, TEST_DATA_PATH, run_pytest


@pytest.fixture
def test_data():
    return TEST_DATA


@pytest.mark.parametrize(
    "path,expected",
    [
        (TEST_DATA_PATH, TEST_DATA),
        (__file__, []),
        ("thisfiledoesntexist.notreal", []),
    ],
)
def test_load_tasks(path, expected):
    data = tasks.load_tasks(path)

    assert data == expected


@pytest.mark.parametrize(
    "task_list,expected",
    [(TEST_DATA, 5), ([], 1)],
)
def test_generate_unique_id(task_list, expected):
    assert tasks.generate_unique_id(task_list) == expected


# fixture + parameterize
@pytest.mark.parametrize(
    "category,expected_indexes",
    [("Work", (0, 3)), ("Personal", (1,)), ("School", (2,))],
)
def test_filter_tasks_by_category(test_data, category, expected_indexes):
    items = tasks.filter_tasks_by_category(test_data, category)

    assert items == [test_data[i] for i in sorted(expected_indexes)]


# fixture + parameterize
@pytest.mark.parametrize(
    "query,expected_indexes",
    [("tHe", (0, 2, 3)), ("TEST", (0, 1, 2, 3)), ("this", (0, 2))],
)
def test_search_tasks(test_data, query, expected_indexes):
    items = tasks.search_tasks(test_data, query)

    assert items == [test_data[i] for i in sorted(expected_indexes)]


def run_tests():
    return run_pytest(__file__)
