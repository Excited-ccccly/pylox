from pylox.expr import ExprVisitor
from pylox.stmt import StmtVisitor
from pylox.token import Token, TokenType
from pylox.error import RuntimeError, ReturnValue
from pylox.environment import Environment
from pylox.lox_callable import LoxCallable, Clock
from pylox.lox_function import LoxFunction
from pylox.lox_class import LoxClass, LoxInstance

class Interpreter(ExprVisitor, StmtVisitor):
  """interpret the ast tree.
  it implement ExprVisitor and StmtVisitor visitor interface.
  """

  def __init__(self):
    self.globals = Environment()
    self.environment = self.globals
    self.globals.define("clock", Clock())
    self.locals = {}

  def interprete(self, stmts):
    try:
      for stmt in stmts:
        self.execute(stmt)
    except RuntimeError as e:
      print(e)

  def execute(self, stmt):
    stmt.accept(self)

  def resolve(self, expr, depth:int):
    self.locals[expr] = depth

  def evaluate(self, expr):
    return expr.accept(self)

  def visit_assign_expr(self, expr):
    value = self.evaluate(expr.value)
    distance = self.locals.get(expr)
    if distance:
      self.environment.assign_at(distance, expr.name.lexeme, value)
    else:
      self.globals.assign(expr.name.lexeme, value)
    return value

  def visit_binary_expr(self, expr):
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
    elif operator_type == TokenType.EQUAL_EQUAL:
      return left == right
    return None

  def visit_call_expr(self, expr):
    callee = self.evaluate(expr.callee)
    arguments = [self.evaluate(arg) for arg in expr.arguments]
    if not isinstance(callee, LoxCallable):
      raise RuntimeError(expr.paren, "Can only call functions and classes.")
    func = callee
    if len(arguments) != func.arity():
      raise RuntimeError(expr.paren, f"Expected {func.arity()} arguments but got {len(arguments)}.")
    return func.call(self, arguments)

  def visit_get_expr(self, expr):
    obj = self.evaluate(expr.object)
    if isinstance(obj, LoxInstance):
      return obj.get(expr.name)
    raise RuntimeError(expr.name, "Only instances have properties.")

  def visit_literal_expr(self, expr):
    return expr.value

  def visit_logical_expr(self, expr):
    left_value = self.evaluate(expr.left)
    if expr.operator.type == TokenType.OR:
      if self.__is_truthy(left_value):
        return left_value
    else:
      if not self.__is_truthy(left_value):
        return left_value
    return self.evaluate(expr.right)

  def visit_grouping_expr(self, expr):
    return self.evaluate(expr.expression)

  def visit_set_expr(self, expr):
    obj = self.evaluate(expr.object)
    if isinstance(obj, LoxInstance):
      value = self.evaluate(expr.value)
      obj.set(expr.name.lexeme, value)
      return value
    raise RuntimeError(expr.name, "Only instances have fields.")

  def visit_super_expr(self, expr):
    distance = self.locals.get(expr)
    superclass: LoxClass = self.environment.get_at(distance, "super")
    instance: LoxInstance = self.environment.get_at(distance - 1, "this")
    method = superclass.find_method(instance, expr.method.lexeme)
    if not method:
      raise RuntimeError(expr.method, f"Undefined property '{expr.method.lexeme}'.")
    return method

  def visit_this_expr(self, expr):
    return self.__lookup_variable(expr.keyword, expr)

  def visit_unary_expr(self, expr):
    right = self.evaluate(expr.right)
    if expr.operator.type == TokenType.MINUS:
      self.__check_number_operands(expr.operator, right)
      return -float(right)
    elif expr.operator.type == TokenType.BANG:
      return not self.__is_truthy(right)
    return None

  def visit_variable_expr(self, expr):
    return self.__lookup_variable(expr.name, expr)

  def __lookup_variable(self, token, expr):
    distance = self.locals.get(expr)
    if distance is not None:
      return self.environment.get_at(distance, token.lexeme)
    else:
      return self.globals.get(token)

  def visit_print_stmt(self, stmt):
    value = self.evaluate(stmt.expression)
    print(value)

  def execute_block(self, stmts, environment):
    previous = self.environment
    try:
      self.environment = environment
      for s in stmts:
        self.execute(s)
    finally:
      self.environment = previous

  def visit_block_stmt(self, stmt):
    block_environment = Environment(enclosing=self.environment)
    self.execute_block(stmt.statements, block_environment)

  def visit_class_stmt(self, stmt):
    superclass = None
    if stmt.superclass:
      superclass = self.evaluate(stmt.superclass)
      if not isinstance(superclass, LoxClass):
        raise RuntimeError(stmt.superclass.name, "Superclass must be a class.")
    lexeme = stmt.name.lexeme
    self.environment.define(lexeme, None)
    if stmt.superclass:
      self.environment = Environment(self.environment)
      self.environment.define("super", superclass)
    methods = {}
    for method in stmt.methods:
      function = LoxFunction(method, self.environment, method.name.lexeme == "init")
      methods[method.name.lexeme] = function
    klass = LoxClass(lexeme, superclass, methods)
    if stmt.superclass:
      self.environment = self.environment.enclosing
    self.environment.assign(lexeme, klass)

  def visit_expression_stmt(self, stmt):
    self.evaluate(stmt.expression)

  def visit_function_stmt(self, stmt):
    func = LoxFunction(stmt, self.environment, False)
    self.environment.define(stmt.name.lexeme, func)

  def visit_if_stmt(self, stmt):
    c = self.evaluate(stmt.condition)
    if self.__is_truthy(c):
      self.execute(stmt.thenBranch)
    elif stmt.elseBranch:
      self.execute(stmt.elseBranch)

  def visit_return_stmt(self, stmt):
    value = None
    if stmt.value:
      value = self.evaluate(stmt.value)
    raise ReturnValue(value)

  def visit_while_stmt(self, stmt):
    while self.__is_truthy(self.evaluate(stmt.condition)):
      self.execute(stmt.body)

  def visit_var_stmt(self, stmt):
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