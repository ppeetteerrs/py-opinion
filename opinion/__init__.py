from contextlib import suppress
from importlib import metadata
from os import system as shell

__author__ = "Peter Yuen"
__email__ = "ppeetteerrsx@gmail.com"
__version__ = "0.0.0"
with suppress(Exception):
    __version__ = metadata.version("opinion")


def __test():  # pragma: no cover
    """
    Runs pytest locally and keeps only `coverage.xml` for GitHub Actions to upload to Codecov.
    """
    shell(
        "pytest --cov=opinion --cov-report xml --cov-report term-missing tests \
            && rm -rf .pytest_cache && rm .coverage"
    )


def __serve():  # pragma: no cover
    """
    Serve local documentation.
    """
    shell(
        "cp README.md docs/index.md && \
            mkdocs serve"
    )


def __docs():  # pragma: no cover
    """
    Build gh-pages documentation branch.
    """
    shell(
        "cp README.md docs/index.md && \
            mkdocs gh-deploy --force"
    )
