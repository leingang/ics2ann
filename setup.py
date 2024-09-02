from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="ics2ann",
    description="Process an ICS feed to generate announcements CSV",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Matthew Leingang",
    url="https://github.com/leingang/ics2ann",
    project_urls={
        "Issues": "https://github.com/leingang/ics2ann/issues",
        "CI": "https://github.com/leingang/ics2ann/actions",
        "Changelog": "https://github.com/leingang/ics2ann/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["ics2ann"],
    entry_points="""
        [console_scripts]
        ics2ann=ics2ann.cli:cli
    """,
    install_requires=["click", "icalevents"],
    extras_require={
        "test": ["pytest"]
    },
    python_requires=">=3.7",
)
