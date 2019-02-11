# -*- coding: utf-8 -*-

"""Console script for pylox."""
import sys
import click

from pylox.error import error_handler
from pylox.scanner import Scanner
from pylox.parser import Parser
from pylox.interpreter import Interpreter
from pylox.resolver import Resolver

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
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    code = '\n'.join(lines)    
    run(code)


def run_file(file):
  with open(file) as f:
      run(f.read())

interpreter = Interpreter()
def run(source: str):
  tokens = Scanner(source).scan_tokens()
  stmts = Parser(tokens).parse()
  if error_handler.had_error: return
  Resolver(interpreter).resolve(stmts)
  if error_handler.had_error: return
  interpreter.interprete(stmts)


if __name__ == "__main__":
  sys.exit(main())  # pragma: no cover
