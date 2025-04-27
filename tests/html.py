from pathlib import Path

import pytest

from tests.common import REPO_DIR

REPORT_PATH = (Path(REPO_DIR) / "temp" / "report.html").resolve()


def generate_html_report(report_path=REPORT_PATH):
    """Generates an HTML report of the tests

    Args:
        report_path (str, optional): The path to save the report to. Defaults to REPORT_PATH.

    Returns:
        str | None: The content of the report, or None
    """
    path = Path(report_path)

    # get rid of old report, if applicable
    if path.exists():
        path.unlink()

    pytest.main([f"--html={report_path}", "--self-contained-html"])

    content = None

    if path.exists():
        with open(report_path, "r") as f:
            content = f.read()
        path.unlink()

    return content
