from pylox.expr import ExprVisitor
from pylox.stmt import StmtVisitor
from pylox.token import Token, TokenType
from pylox.error import RuntimeError
from pylox.environment import Environment

class Interpreter(ExprVisitor, StmtVisitor):

  def __init__(self):
    self.environment = Environment()

  def interprete(self, stmts):
    try:
      for stmt in stmts:
        self.execute(stmt)
    except RuntimeError as e:
      print(e)

  def execute(self, stmt):
    stmt.accept(self)

  def evaluate(self, expr):
    return expr.accept(self)

  def visitBinaryExpr(self, expr):
    left = self.evaluate(expr.left)
    right = self.evaluate(expr.right)
    operator_type = expr.operator.type
    if operator_type == TokenType.MINUS:
      self.__check_number_operands(expr.operator, left, right)
      return float(left) - float(right)
    elif operator_type == TokenType.SLASH:
      self.__check_number_operands(expr.operator, left, right)
      return float(left) / float(right)
    elif operator_type == TokenType.STAR:
      self.__check_number_operands(expr.operator, left, right)
      return float(left) * float(right)
    elif operator_type == TokenType.PLUS:
      if isinstance(left, float) and isinstance(right, float):
        return float(left) + float(right)
      if (isinstance(left, str) or isinstance(left, float)) and (isinstance(right, str), isinstance(right, float)):
        return str(left)+str(right)
      raise RuntimeError("Operand must be number or string")
    elif operator_type == TokenType.GREATER:
      self.__check_number_operands(expr.operator, left, right)
      return float(left) > float(right)
    elif operator_type == TokenType.GREATER_EQUAL:
      self.__check_number_operands(expr.operator, left, right)
      return float(left) >= float(right)
    elif operator_type == TokenType.LESS:
      self.__check_number_operands(expr.operator, left, right)
      return float(left) < float(right)
    elif operator_type == TokenType.LESS_EQUAL:
      self.__check_number_operands(expr.operator, left, right)
      return float(left) <= float(right)
    elif operator_type == TokenType.BANG_EQUAL:
      return not left == right
    elif operator_type == TokenType.BANG_EQUAL:
      return left == right
    return None

  def visitLiteralExpr(self, expr):
    return expr.value

  def visitGroupingExpr(self, expr):
    return self.evaluate(expr.expression)
  
  def visitUnaryExpr(self, expr):
    right = self.evaluate(expr.right)
    if expr.operator.type == TokenType.MINUS:
      self.__check_number_operands(expr.operator, right)
      return -float(right)
    elif expr.operator.type == TokenType.BANG:
      return not self.__is_truthy(right)
    return None
  
  def visitVariableExpr(self, expr):
    return self.environment.get(expr.name)

  def visitPrintStmt(self, stmt):
    value = self.evaluate(stmt.expression)
    print(value)

  def visitExpressionStmt(self, stmt):
    self.evaluate(stmt.expression)

  def visitVarStmt(self, stmt):
    value = None
    if stmt.initializer:
      value = self.evaluate(stmt.initializer)
    self.environment.define(stmt.name.lexeme, value)

  def __is_truthy(self, obj):
    if obj == None: return False
    if isinstance(obj, bool): return bool(obj)
    return True

  def __check_number_operands(self, operator, *operands):
    if (all(isinstance(o, float) for o in operands)): return
    raise RuntimeError("Operand must be a number")