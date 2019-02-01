from pylox.visitor import ExprVisitor
from pylox.token import Token, TokenType

class Interpreter(ExprVisitor):

  class RuntimeError(Exception):
    pass

  def interprete(self, expr):
    try:
      return self.evaluate(expr)
    except Interpreter.RuntimeError as e:
      print(e)

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
      raise Interpreter.RuntimeError("Operand must be number or string")
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

  def __is_truthy(self, obj):
    if obj == None: return False
    if isinstance(obj, bool): return bool(obj)
    return True

  def __check_number_operands(self, operator, *operands):
    if (all(isinstance(o, float) for o in operands)): return
    raise Interpreter.RuntimeError("Operand must be a number")