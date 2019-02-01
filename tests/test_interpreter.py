from typing import List
from unittest import TestCase
from pylox.scanner import Scanner
from pylox.parser import Parser
from pylox.ast_printer import AstPrinter
from pylox.interpreter import Interpreter

class TestParser(TestCase):
  def setUp(self):
    with open("tests/data/test_parser.lox") as f:
      scanner = Scanner(f.read())
      tokens = scanner.scan_tokens()
      parser = Parser(tokens)
      self.expr = parser.parse()
      
  def test_expr_parser(self):
    result = Interpreter().interprete(self.expr)
    self.assertEqual(0, result)