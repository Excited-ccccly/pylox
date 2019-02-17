from typing import List
from tests.test_base import LoxTestBase
from pylox.scanner import Scanner
from pylox.parser import Parser
from pylox.ast_printer import AstPrinter

class TestParser(LoxTestBase):

  def test_expr_parser(self):
    with open("tests/data/test_parser.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      expr = stmts[0].expression
      s = expr.accept(AstPrinter())
      self.assertEqual('(+ (+ 3.0 (/ 6.0 (- 3.0))) (- 1.0))', s)

  def test_parse_error_at_eof(self):
    with self.assertStdout() as output:
      Parser(Scanner("var a=1;var b=2;print a+b").scan_tokens()).parse()
      self.assertEqual("[line1] Error.  at end: Expect ';' after statement.\n", output.getvalue())


