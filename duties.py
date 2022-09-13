"""Development tasks."""

import os
import sys
from pathlib import Path

from duty import duty

PY_SRC_PATHS = (Path(_) for _ in ("src", "tests", "duties.py"))
PY_SRC_LIST = tuple(str(_) for _ in PY_SRC_PATHS)
PY_SRC = " ".join(PY_SRC_LIST)


@duty
def check_quality(ctx):
    """
    Check the code quality

    Arguments:
        ctx: The context instance (passed automatically)
    """
    ctx.run(
        f"flake8 --config=config/flake8.ini {PY_SRC}",
        title="Checking code quality",
        nofail=True,
        quiet=False,
    )


@duty
def check_types(ctx):
    """
    Check that the code is correctly typed.

    Arguments:
        ctx: The context instance (passed automatically)
    """
    ctx.run(
        f"mypy --config-file config/mypy.ini {PY_SRC}",
        title="Checking types",
        nofail=True,
        quiet=True,
    )


@duty(silent=True)
def coverage(ctx):
    """
    Report coverage as text and HTML.

    Arguments:
        ctx: The context instance (passed automatically)
    """
    ctx.run("coverage combine", nofail=True)
    ctx.run("coverage report --rcfile=config/coverage.ini", capture=False)
    ctx.run("coverage json --rcfile=config/coverage.ini")


@duty
def format(ctx):
    """
    Run formatting tools on the code

    Arguments:
        ctx: The context instance (passed automatically)
    """
    ctx.run(f"isort {PY_SRC}", title="Ordering imports")
    ctx.run(f"black {PY_SRC}", title="Formatting code")


@duty
def test(ctx, match=""):
    """
    Run the test suite.

    Arguments:
        ctx: The context instance (passed automatically)
        match: A pytest expression to filter selected tests.
    """
    py_version = f"{sys.version_info.major}{sys.version_info.minor}"
    os.environ["COVERAGE_FILE"] = f".coverage.{py_version}"
    ctx.run(
        ["pytest", "-c", "config/pytest.ini", "tests"],
        title="Running tests",
    )


@duty(silent=True)
def clean(ctx):
    """
    Delete temporary files

    Arguments:
        ctx: The context instance (passed automatically)
    """
    ctx.run("rm -rf .coverage*")
    ctx.run("rm -rf .mypy_cache")
    ctx.run("rm -rf .pytest_cache")
    ctx.run("rm -rf tests/.pytest_cache")
    ctx.run("rm -rf cov")
    ctx.run("rm -rf dist")
    ctx.run("rm -rf build")
    ctx.run("find . -type d -name __pycache__ | xargs rm -rf")
    ctx.run("find . -name '*.rej' -delete")
