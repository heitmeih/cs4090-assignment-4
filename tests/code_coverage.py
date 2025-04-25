import os

import coverage
import pytest

from tests.common import SRC_DIR, TEST_DIR

cov = coverage.Coverage(source=[SRC_DIR])


def get_code_coverage():
    """Runs code coverage for all tests.

    Returns:
        list[tuple[str, int]]: a list of (filename, coverage %) pairs
    """
    cov.start()

    pytest.main([TEST_DIR])

    # Stop coverage and save data
    cov.stop()

    # Access coverage stats
    data = cov.get_data()
    covered_files = data.measured_files()

    coverage_reports = []

    # Process stats for each file
    for filename in covered_files:
        _, executed, excluded, not_executed, _ = cov.analysis2(filename)
        num_executed = len(executed)
        num_excluded = len(excluded)
        num_not_executed = len(not_executed)

        total_lines = num_executed + num_excluded + num_not_executed
        covered = total_lines - num_not_executed
        coverage_percent = 100.0 * (covered / total_lines) if total_lines > 0 else 0
        coverage_reports.append((os.path.basename(filename), coverage_percent))

    return coverage_reports
