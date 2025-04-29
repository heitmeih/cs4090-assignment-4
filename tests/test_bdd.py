from pathlib import Path

from tests.common import run_pytest


def run_tests():
    return run_pytest(str(Path(__file__).resolve().parent / "feature"))
