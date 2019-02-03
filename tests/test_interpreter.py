from typing import List
from unittest import TestCase
from pylox.scanner import Scanner
from pylox.parser import Parser
from pylox.ast_printer import AstPrinter
from pylox.interpreter import Interpreter

class TestInterpreter(TestCase):
  def setUp(self):
    with open("tests/data/test_interpreter.lox") as f:
      scanner = Scanner(f.read())
      tokens = scanner.scan_tokens()
      parser = Parser(tokens)
      self.stmts = parser.parse()
      
  def test_stmts_interpret(self):
    Interpreter().interprete(self.stmts)