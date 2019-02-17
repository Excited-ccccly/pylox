from tests.test_base import LoxTestBase
from pylox.expr import Assign, Binary, Unary, Literal, Grouping
from pylox.token import Token, TokenType
from pylox.ast_printer import AstPrinter
from pylox.scanner import Scanner
from pylox.parser import Parser


class TestAstPrinter(LoxTestBase):

  def test_ast_printer(self):
    unary = Unary(operator=Token(TokenType.MINUS, "-", None, 1),
                  right=Literal(value=123))
    expr = Binary(left=unary,
                  operator=Token(TokenType.STAR, "*", None, 1),
                  right=Grouping(expression=Literal(value=45.67)))
    printer = AstPrinter()
    self.assertEqual('(* (- 123) (group 45.67))', printer.print(expr))
    with open("tests/data/test_ast_printer.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      output = [printer.print(stmt) for stmt in stmts]
      self.assertTrue(len(output) > 0)