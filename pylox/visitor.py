from abc import abstractmethod
from expr import Expr

class ExprVisitor:
  @abstractmethod
  def visitAssignExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitBinaryExpr(self, expr):
    raise NotImplementedError()    

class AstPrinter(ExprVisitor):
  def print(self, expr: Expr):
    expr.accept(self)

  def visitAssignExpr(self, expr):
    print(f"Astprinter:{expr.name}={expr.value}")
