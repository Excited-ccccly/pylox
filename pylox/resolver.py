from typing import List
from enum import IntEnum

from pylox.expr import ExprVisitor
from pylox.stmt import StmtVisitor
from pylox.token import Token, TokenType
from pylox.error import error_handler

class Resolver(ExprVisitor, StmtVisitor):
  """A semantic analyzer to figure out how many hops between a variable's declaration and usage.
  resolver will put those hops data into interpreter.
  """

  def __init__(self, interpreter):
    self.interpreter = interpreter
    self.scopes: List[dict] = []
    self.current_function = FunctionType.NONE
    self.current_class = ClassType.NONE

  def visit_block_stmt(self, stmt):
    self.__begin_scope()
    self.resolve(stmt.statements)
    self.__end_scope()

  def visit_var_stmt(self, stmt):
    self.__declare(stmt.name)
    if stmt.initializer:
      self.__resolve(stmt.initializer)
    self.__define(stmt.name)

  def visit_variable_expr(self, expr):
    if self.scopes and self.scopes[-1].get(expr.name.lexeme) == False:
      error_handler.resolve_error(expr.name, "Cannot read local variable in its own initializer.")
    self.__resolve_local(expr, expr.name)

  def visit_assign_expr(self, expr):
    self.__resolve(expr.value)
    self.__resolve_local(expr, expr.name)

  def visit_class_stmt(self, stmt):
    enclosing_class = self.current_class
    self.current_class = ClassType.CLASS
    self.__declare(stmt.name)
    if stmt.superclass:
      self.current_class = ClassType.SUBCLASS
      self.__resolve(stmt.superclass)
    self.__define(stmt.name)
    if stmt.superclass:
      self.__begin_scope()
      self.scopes[-1]["super"] = True
    self.__begin_scope()
    self.scopes[-1]["this"] = True
    for method in stmt.methods:
      func_type = FunctionType.METHOD
      if method.name.lexeme == "init":
        func_type = FunctionType.INITIALIZER
      self.__resolve_function(method, func_type)
    self.__end_scope()
    if stmt.superclass:
      self.__end_scope()
    self.current_class = enclosing_class

  def visit_function_stmt(self, stmt):
    self.__declare(stmt.name)
    self.__define(stmt.name)
    self.__resolve_function(stmt, FunctionType.FUNCTION)

  def visit_expression_stmt(self, stmt):
    self.__resolve(stmt.expression)

  def visit_if_stmt(self, stmt):
    self.__resolve(stmt.condition)
    self.__resolve(stmt.thenBranch)
    if stmt.elseBranch:
      self.__resolve(stmt.elseBranch)

  def visit_print_stmt(self, stmt):
    self.__resolve(stmt.expression)

  def visit_return_stmt(self, stmt):
    if self.current_function == FunctionType.NONE:
      error_handler.resolve_error(stmt.keyword, "Cannot return from top-level code.")
    if stmt.value:
      if self.current_function == FunctionType.INITIALIZER:
        error_handler.resolve_error(stmt.keyword, "Cannot return a value from an initializer.")
      self.__resolve(stmt.value)

  def visit_while_stmt(self, stmt):
    self.__resolve(stmt.condition)
    self.__resolve(stmt.body)

  def visit_binary_expr(self, expr):
    self.__resolve(expr.left)
    self.__resolve(expr.right)

  def visit_call_expr(self, expr):
    self.__resolve(expr.callee)
    for argument in expr.arguments:
      self.__resolve(argument)

  def visit_get_expr(self, expr):
    self.__resolve(expr.object)

  def visit_grouping_expr(self, expr):
    self.__resolve(expr.expression)

  def visit_literal_expr(self, expr):
    pass

  def visit_logical_expr(self, expr):
    self.__resolve(expr.left)
    self.__resolve(expr.right)

  def visit_set_expr(self, expr):
    self.__resolve(expr.value)
    self.__resolve(expr.object)

  def visit_super_expr(self, expr):
    if self.current_class == ClassType.NONE:
      error_handler.resolve_error(expr.keyword, "Cannot use 'super' outside of a class.")
    elif self.current_class != ClassType.SUBCLASS:
      error_handler.resolve_error(expr.keyword, "Cannot use 'super' in a class with no superclass.")
    self.__resolve_local(expr, expr.keyword)

  def visit_this_expr(self, expr):
    if self.current_class == ClassType.NONE:
      error_handler.resolve_error(expr.keyword, "Cannot use 'this' outside of a class.")
      return
    self.__resolve_local(expr, expr.keyword)

  def visit_unary_expr(self, expr):
    self.__resolve(expr.right)

  def __resolve_function(self, func_stmt, func_type):
    enclosing_function = self.current_function
    self.current_function = func_type
    self.__begin_scope()
    for param in func_stmt.params:
      self.__declare(param.name)
      self.__define(param.name)
    self.resolve(func_stmt.body.statements)
    self.__end_scope()
    self.current_function = enclosing_function

  def __resolve_local(self, expr, token):
    for i in reversed(range(0, len(self.scopes))):
      if self.scopes[i].__contains__(token.lexeme):
        self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
        return

  def __declare(self, name: Token):
    if self.scopes:
      scope = self.scopes[-1]
      if scope.__contains__(name.lexeme):
        error_handler.resolve_error(name, "Variable with this name already declared in this scope.")
      scope[name.lexeme] = False

  def __define(self, name: Token):
    if self.scopes:
      scope = self.scopes[-1]
      scope[name.lexeme] = True

  def __begin_scope(self):
    self.scopes.append({})

  def __end_scope(self):
    self.scopes.pop()

  def resolve(self, stmts):
    for stmt in stmts:
      self.__resolve(stmt)

  def __resolve(self, stmt_or_expr):
    stmt_or_expr.accept(self)

class FunctionType(IntEnum):
  NONE = 0
  FUNCTION = 1
  METHOD = 2
  INITIALIZER = 3

class ClassType(IntEnum):
  NONE = 0
  CLASS = 1
  SUBCLASS = 2