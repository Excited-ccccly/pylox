from unittest import TestCase
from pylox.expr import Assign
from pylox.visitor import AstPrinter

class TestExpr(TestCase):

  def test_assign(self):
    a = Assign("a", 1)
    a.accept(AstPrinter())