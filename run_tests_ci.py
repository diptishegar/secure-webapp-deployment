#!/usr/bin/env python3
"""
CI test runner: runs pytest and exits with pytest's exit code.

Usage:
  python run_tests_ci.py [pytest-args...]

Environment variables:
  TEST_PATH  - path or module to test (default: "tests")
  JUNIT_XML  - optional path to write JUnit XML results (useful for CI)

This script is intended to be invoked from a GitHub Actions job (or any CI).
It prints the pytest arguments it's using and exits with the same return code
so CI jobs will fail when tests fail.
"""
import os
import sys
import pytest


def main(argv=None):
    argv = list(argv or sys.argv[1:])

    test_path = os.environ.get("TEST_PATH", "tests")
    junit_xml = os.environ.get("JUNIT_XML")

    pytest_args = []
    if junit_xml:
        pytest_args += ["--junitxml", junit_xml]

    # default: quiet, run the configured test path
    pytest_args += ["-q", test_path]

    # append any extra args passed to this script
    if argv:
        pytest_args += argv

    print("Running pytest with:", pytest_args, file=sys.stderr)

    # run pytest and propagate exit code
    rc = pytest.main(pytest_args)
    sys.exit(rc)


if __name__ == "__main__":
    main()
