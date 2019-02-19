from pylox.expr import Expr
from pylox.token import Token
from pylox.expr import ExprVisitor
from pylox.stmt import StmtVisitor

class AstPrinter(ExprVisitor, StmtVisitor):
  """print the ast tree.
  implement ExprVisitor and StmtVisitor visitor interface.
  """
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

  def visit_block_stmt(self, stmt):
    stmts = "".join([stmt.accept(self) for stmt in stmt.statements])
    return f"(block {stmts})"

  def visit_class_stmt(self, stmt):
    name = f"(class {stmt.name.lexeme}"
    if stmt.superclass:
      name += f" < {stmt.superclass.accept(self)}"
    methods = " ".join([method.accept(self) for method in stmt.methods])
    return f"{name} {methods})"

  def visit_expression_stmt(self, stmt):
    return self.parenthesize(";", stmt.expression)

  def visit_function_stmt(self, stmt):
    name = f"(func {stmt.name.lexeme}("
    tokens = " ".join([param.name.lexeme for param in stmt.params])
    body = "".join([s.accept(self) for s in stmt.body.statements])
    return f"{name}{tokens}){body})"

  def visit_if_stmt(self, stmt):
    if stmt.elseBranch:
      return self.parenthesize2("if-else", stmt.condition, stmt.thenBranch, stmt.elseBranch)
    return self.parenthesize("if", stmt.condition, stmt.thenBranch)

  def visit_print_stmt(self, stmt):
    return self.parenthesize("print", stmt.expression)

  def visit_return_stmt(self, stmt):
    if stmt.value:
      return self.parenthesize("return", stmt.value)
    return "(return)"

  def visit_var_stmt(self, stmt):
    if stmt.initializer:
      return self.parenthesize2("var", stmt.name, "=", stmt.initializer)
    return self.parenthesize2("var", stmt.name)

  def visit_while_stmt(self, stmt):
    return self.parenthesize2("while", stmt.condition, stmt.body)


