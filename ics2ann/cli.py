import csv
import datetime
import logging

import click
import icalevents.icalevents as icalevents

from .events import Event
from .dateutils import end_of_year
from .announcements import announcements_from_events, officehours_from_events, CsvWriter, TexWriter


@click.group()
@click.version_option()
def cli():
    "Process an ICS feed to generate announcements CSV"


@cli.command(name="read", help="Read iCal events from INPUT and create Announcements")
@click.argument("input")
@click.option(
    "--output",
    "-o",
    type=click.File("w"),
    default="-",
    help="Write output to FILENAME (default: stdout)",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "tex"], case_sensitive=False),
    default="csv",
    help="Output file format (default:csv)",
)
@click.option(
    "--start",
    type=click.DateTime(),
    default=datetime.date.today().isoformat(),
    help="Find events after this date (default: today)",
)
@click.option(
    "--end",
    type=click.DateTime(),
    default=end_of_year(datetime.date.today()).isoformat(),
    help="Find events before this date (default: end of current year)",
)
@click.option("--headers/--no-headers", default=True, help="Include the header row")
def read_ics(input, output, format, start, end, headers):
    click.echo(f"{input=}, {headers=}", err=True)
    events = [Event(e) for e in icalevents.events(input, start=start, end=end)]
    writer_classes = {"tex": TexWriter, "csv": CsvWriter}
    writer_class = writer_classes[format]
    writer = writer_class(output, headers=headers)
    for a in sorted(announcements_from_events(events), key=lambda x: (x.end, x.text)):
        writer.write(a)


@cli.command(name="readoh", help="Read Office Hours iCal events from INPUT and create Announcements")
@click.argument("input")
@click.option(
    "--output",
    "-o",
    type=click.File("w"),
    default="-",
    help="Write output to FILENAME (default: stdout)",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "tex"], case_sensitive=False),
    default="csv",
    help="Output file format (default:csv)",
)
@click.option(
    "--start",
    type=click.DateTime(),
    default=datetime.date.today().isoformat(),
    help="Find events after this date (default: today)",
)
@click.option(
    "--end",
    type=click.DateTime(),
    default=end_of_year(datetime.date.today()).isoformat(),
    help="Find events before this date (default: end of current year)",
)
@click.option("--headers/--no-headers", default=True, help="Include the header row")
def read_ics_oh(input, output, format, start, end, headers):
    click.echo(f"{input=}, {headers=}", err=True)
    events = [Event(e) for e in icalevents.events(input, start=start, end=end)]
    writer_classes = {"tex": TexWriter, "csv": CsvWriter}
    writer_class = writer_classes[format]
    writer = writer_class(output, headers=headers)
    for a in sorted(officehours_from_events(events), key=lambda x: (x.end, x.start)):
        writer.write(a)