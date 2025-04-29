from pytest_bdd import given, scenario, then, when

from src import tasks
from tests.common import TEST_DATA


@scenario("sort.feature", "Sorting by due date, descending")
def test_sort_by_due_date():
    pass


@given("I am using the test data", target_fixture="test_data")
def get_test_data():
    return [task.copy() for task in TEST_DATA]


@given("I sort by due date", target_fixture="sort_by")
def get_sort_by():
    return "due_date"


@given("I sort in descending order", target_fixture="asc")
def get_asc():
    return False


@when("I sort the data", target_fixture="result")
def do_sort(test_data, sort_by, asc):
    return tasks.sort_tasks(test_data, sort_by, asc)


@then("The result should be organized from highest due date to lowest")
def check_result(test_data, result):
    assert result == [test_data[i] for i in (1, 3, 0, 2)]
