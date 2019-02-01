from unittest import TestCase
from pylox.expr import Assign, Binary, Unary, Literal, Grouping
from pylox.token import Token, TokenType
from pylox.visitor import AstPrinter

class TestExpr(TestCase):

  def test_assign(self):
    unary = Unary(operator=Token(TokenType.MINUS, "-", None, 1),
                  right=Literal(value=123))
    expr = Binary(left=unary,
                  operator=Token(TokenType.STAR, "*", None, 1),
                  right=Grouping(expression=Literal(value=45.67)))
    self.assertEqual('(* (- 123) (group 45.67))', expr.accept(AstPrinter()))
      