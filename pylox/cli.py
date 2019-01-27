# -*- coding: utf-8 -*-

"""Console script for pylox."""
import sys
import click

from pylox.scanner import Scanner


@click.command()
@click.argument('file', type=click.Path(exists=True), required=False)
def main(file=None):
  """Console script for pylox."""
  if not file:
      run_repr()
  run_file(file)
  return 0


def run_repr():

  while True:
      print("> ", end="")
      run(input())


def run_file(file):
  with open(file) as f:
      run(f.read())


def run(source: str):
  scanner = Scanner(source)
  print(scanner.scan_tokens())


if __name__ == "__main__":
  sys.exit(main())  # pragma: no cover
