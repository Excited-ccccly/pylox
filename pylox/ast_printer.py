from pylox.expr import Expr
from pylox.token import Token
from pylox.visitor import ExprVisitor

class AstPrinter(ExprVisitor):
  def print(self, expr: Expr):
    return expr.accept(self)

  def parenthesize(self, name, *exprs):
    expr_str = " ".join([expr.accept(self) for expr in exprs])
    return f"({name} {expr_str})"

  def parenthesize2(self, name, *parts):
    def inner(part):
      if isinstance(part, Expr):
        return part.accept(self)
      elif isinstance(part, Token):
        return part.lexeme
      else:
        return str(part)
    expr_str = " ".join(inner(part) for part in parts)
    return f"({name} {expr_str})"


  def visitAssignExpr(self, expr):
    return self.parenthesize2("=", expr.name.lexeme, expr.value)
  
  def visitBinaryExpr(self, expr):
    return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

  def visitCallExpr(self, expr):
    return self.parenthesize2("call", expr.callee, expr.arguments)

  def visitGetExpr(self, expr):
    return self.parenthesize2(".", expr.object, expr.name.lexeme)
  
  def visitGroupingExpr(self, expr):
    return self.parenthesize("group", expr.expression)

  def visitLiteralExpr(self, expr):
    if expr.value is None: return "nil"
    return str(expr.value)

  def visitLogicalExpr(self, expr):
    return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

  def visitSetExpr(self, expr):
    return self.parenthesize2("=",
        expr.object, expr.name.lexeme, expr.value)

  def visitSuperExpr(self, expr):
    return self.parenthesize2("super", expr.method)

  def visitThisExpr(self, expr):
    return 'this'

  def visitUnaryExpr(self, expr):
    return self.parenthesize(expr.operator.lexeme, expr.right)

  def visitVariableExpr(self, expr):
    return expr.name.lexeme