"""Unit Testing"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from common import TEST_DATA, TEST_DATA_PATH, run_pytest

from src import tasks

parent_dir = Path(__file__).parent.resolve()


def test_load_tasks_success():
    data = tasks.load_tasks(TEST_DATA_PATH)

    assert data == TEST_DATA


def test_load_tasks_parse_error():
    data = tasks.load_tasks(__file__)

    assert data == []


def test_load_tasks_file_not_found_error():
    data = tasks.load_tasks("doesnotexist.notreal")

    assert data == []


def test_save_tasks():
    savefile = str(parent_dir / "temp.json")

    tasks.save_tasks(TEST_DATA, savefile)

    try:
        with open(savefile, "r") as f:
            saved = f.read()
    except:
        raise
    finally:
        os.remove(savefile)

    assert saved == json.dumps(TEST_DATA, indent=2)


def test_generate_unique_id():
    id_ = tasks.generate_unique_id(TEST_DATA)

    assert id_ == 5


def test_filter_tasks_by_priority():
    items = tasks.filter_tasks_by_priority(TEST_DATA, "High")

    assert items == [TEST_DATA[2]]


def test_filter_tasks_by_category():
    items = tasks.filter_tasks_by_category(TEST_DATA, "Work")

    assert items == [TEST_DATA[0], TEST_DATA[3]]


def test_filter_tasks_by_completion():
    items = tasks.filter_tasks_by_completion(TEST_DATA)

    assert items == [TEST_DATA[1], TEST_DATA[3]]


def test_search_tasks():
    items = tasks.search_tasks(TEST_DATA, "tHe")

    assert items == [TEST_DATA[0], TEST_DATA[2], TEST_DATA[3]]


def test_get_overdue_tasks():

    tomorrow = (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d")
    data = [
        TEST_DATA[2],  # very overdue
        {
            "id": 5,
            "title": "Test 5",
            "description": "This task is due tomorrow",
            "priority": "Low",
            "category": "Work",
            "due_date": tomorrow,
            "completed": False,
            "created_at": "2025-04-10 17:54:06",
        },
    ]

    items = tasks.get_overdue_tasks(data)

    assert items == [TEST_DATA[2]]


def run_tests():
    return run_pytest(__file__)
