from pytest_bdd import given, scenario, then, when

from src import tasks
from tests.common import TEST_DATA


@scenario("sort.feature", "Sorting by id, ascending")
def test_sort_by_id():
    pass


@given("I am using the test data", target_fixture="test_data")
def get_test_data():
    return [task.copy() for task in TEST_DATA]


@given("I sort by id", target_fixture="sort_by")
def get_sort_by():
    return "id"


@given("I sort in ascending order", target_fixture="asc")
def get_asc():
    return True


@when("I sort the data", target_fixture="result")
def do_sort(test_data, sort_by, asc):
    return tasks.sort_tasks(test_data, sort_by, asc)


@then("The result should be the same as the test data")
def check_result(test_data, result):
    assert test_data == result
