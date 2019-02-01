from typing import List
from unittest import TestCase
from pylox.scanner import Scanner
from pylox.parser import Parser
from pylox.visitor import AstPrinter

class TestParser(TestCase):
  def setUp(self):
    with open("tests/data/test_parser.lox") as f:
      scanner = Scanner(f.read())
      tokens = scanner.scan_tokens()
      self.parser = Parser(tokens)
      
  def test_expr_parser(self):
    expr = self.parser.parse()
    s = expr.accept(AstPrinter())
    self.assertEqual('(+ (+ 3.0 (/ 6.0 (- 3.0))) (- 1.0))', s)

  def tearDown(self):
    self.parser = None
