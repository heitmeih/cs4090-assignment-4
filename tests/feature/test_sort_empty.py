import random

from pytest_bdd import given, scenario, then, when

from src import tasks


@scenario("sort.feature", "Sorting empty list")
def test_sort_empty():
    pass


@given("I am using an empty list", target_fixture="test_data")
def get_test_data():
    return []


@given("I sort by anything", target_fixture="sort_by")
def get_sort_by():
    return "".join(
        [
            random.choice("abcdefghijklmnopqrstuvqxyz_")
            for _ in range(random.randint(1, 200))
        ]
    )


@given("I sort in any order", target_fixture="asc")
def get_asc():
    return random.choice([True, False])


@when("I sort the data", target_fixture="result")
def do_sort(test_data, sort_by, asc):
    return tasks.sort_tasks(test_data, sort_by, asc)


@then("The result should be an empty list")
def check_result(result):
    assert result == []
