import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parents[1]))
print(sys.path)


class TestReporter:
    def __init__(self):
        self.reports = set()

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            self.reports.add((report.nodeid, report.passed))


def run_pytest(file):
    reporter = TestReporter()
    pytest.main([file], plugins=[reporter])
    return reporter.reports


TEST_DATA = [
    {
        "id": 1,
        "title": "Test 1",
        "description": "This is the first test",
        "priority": "Low",
        "category": "Work",
        "due_date": "2025-04-23",
        "completed": False,
        "created_at": "2025-04-10 17:54:06",
    },
    {
        "id": 2,
        "title": "Test 2",
        "description": "Second test",
        "priority": "Medium",
        "category": "Personal",
        "due_date": "2026-04-10",
        "completed": True,
        "created_at": "2025-04-10 17:54:10",
    },
    {
        "id": 3,
        "title": "Test 3",
        "description": "This is THE TEST",
        "priority": "High",
        "category": "School",
        "due_date": "1900-04-10",
        "completed": False,
        "created_at": "2025-04-10 17:54:16",
    },
    {
        "id": 4,
        "title": "The Test 4",
        "description": "Fourth test",
        "priority": "Low",
        "category": "Work",
        "due_date": "2025-04-24",
        "completed": True,
        "created_at": "2025-04-22 00:00:00",
    },
]

TEST_DATA_PATH: str = str(Path(__file__).parent / "test_data.json")
