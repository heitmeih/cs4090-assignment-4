from pytest_bdd import given, parsers, scenario, then, when

from src import tasks


@scenario("stats.feature", "Empty list stats")
def test_test_data_stats():
    pass


@given("I am using an empty list", target_fixture="test_data")
def get_test_data():
    return []


@when("I fetch its stats", target_fixture="result")
def do_sort(test_data):
    return tasks.get_task_stats(test_data)


@then(
    parsers.parse(
        "The result should be {total:d} total, {completed:d} completed, {incomplete:d} incomplete, and {overdue:d} overdue"
    )
)
def check_result(result, total, completed, incomplete, overdue):
    assert result == (total, incomplete, completed, overdue)
