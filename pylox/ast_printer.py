from pylox.expr import Expr
from pylox.token import Token
from pylox.expr import ExprVisitor

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


  def visit_assign_expr(self, expr):
    return self.parenthesize2("=", expr.name.lexeme, expr.value)

  def visit_binary_expr(self, expr):
    return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

  def visit_call_expr(self, expr):
    return self.parenthesize2("call", expr.callee, expr.arguments)

  def visit_get_expr(self, expr):
    return self.parenthesize2(".", expr.object, expr.name.lexeme)

  def visit_grouping_expr(self, expr):
    return self.parenthesize("group", expr.expression)

  def visit_literal_expr(self, expr):
    if expr.value is None: return "nil"
    return str(expr.value)

  def visit_logical_expr(self, expr):
    return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

  def visit_set_expr(self, expr):
    return self.parenthesize2("=",
        expr.object, expr.name.lexeme, expr.value)

  def visit_super_expr(self, expr):
    return self.parenthesize2("super", expr.method)

  def visit_this_expr(self, expr):
    return 'this'

  def visit_unary_expr(self, expr):
    return self.parenthesize(expr.operator.lexeme, expr.right)

  def visit_variable_expr(self, expr):
    return expr.name.lexeme