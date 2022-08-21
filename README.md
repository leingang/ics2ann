# ics2ann

[![PyPI](https://img.shields.io/pypi/v/ics2ann.svg)](https://pypi.org/project/ics2ann/)
[![Changelog](https://img.shields.io/github/v/release/leingang/ics2ann?include_prereleases&label=changelog)](https://github.com/leingang/ics2ann/releases)
[![Tests](https://github.com/leingang/ics2ann/workflows/Test/badge.svg)](https://github.com/leingang/ics2ann/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/leingang/ics2ann/blob/master/LICENSE)

Process an ICS feed to generate announcements CSV

## Installation

Install this tool using `pip`:

    pip install ics2ann

## Usage

For help, run:

    ics2ann --help

You can also use:

    python -m ics2ann --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd ics2ann
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
