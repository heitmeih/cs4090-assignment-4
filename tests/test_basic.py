"""Unit Testing"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from src import tasks
from tests.common import TEST_DATA, TEST_DATA_PATH, run_pytest

parent_dir = Path(__file__).parent.resolve()


def test_load_tasks_success():
    data = tasks.load_tasks(TEST_DATA_PATH)

    assert data == TEST_DATA


def test_load_tasks_parse_error():
    # try to parse this file
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
    data = [*TEST_DATA, {"title": "No ID"}]

    id_ = tasks.generate_unique_id(data)

    assert id_ == 5
    assert tasks.generate_unique_id([]) == 1


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

    tomorrow = (datetime.now() + timedelta(days=1)).strftime(tasks.DATE_FORMAT)
    yesterday = (datetime.now() - timedelta(days=1)).strftime(tasks.DATE_FORMAT)

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
        {
            "id": 6,
            "title": "Test 6",
            "description": "This task was due yesterday",
            "priority": "High",
            "category": "Work",
            "due_date": yesterday,
            "completed": False,
            "created_at": "2025-04-10 17:54:06",
        },
        {
            "id": 7,
            "title": "Test 7",
            "description": "This task is missing a due date",
            "priority": "High",
            "category": "Work",
            "completed": False,
            "created_at": "2025-04-10 17:54:06",
        },
        {
            "id": 8,
            "title": "Test 8",
            "description": "This task was due yesterday but is completed",
            "priority": "High",
            "category": "Work",
            "due_date": yesterday,
            "completed": True,
            "created_at": "2025-04-10 17:54:06",
        },
        {
            "id": 9,
            "title": "Test 9",
            "description": "This task has the incorrect date format",
            "priority": "High",
            "category": "Work",
            "due_date": "burger",
            "completed": False,
            "created_at": "2025-04-10 17:54:06",
        },
    ]

    items = tasks.get_overdue_tasks(data)

    assert items == [TEST_DATA[2], data[2]]


def run_tests():
    return run_pytest(__file__)
