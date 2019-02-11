from typing import List
from enum import IntEnum

from pylox.expr import ExprVisitor
from pylox.stmt import StmtVisitor
from pylox.token import Token, TokenType
from pylox.error import error_handler

class Resolver(ExprVisitor, StmtVisitor):

  def __init__(self, interpreter):
    self.interpreter = interpreter
    self.scopes: List[dict] = []
    self.current_function = FunctionType.NONE

  def visitBlockStmt(self, stmt):
    self.__begin_scope()
    self.resolve(stmt.statements)
    self.__end_scope()

  def visitVarStmt(self, stmt):
    self.__declare(stmt.name)
    if stmt.initializer:
      self.__resolve(stmt.initializer)
    self.__define(stmt.name)

  def visitVariableExpr(self, expr):
    if self.scopes and self.scopes[-1].get(expr.name.lexeme) == False:
      error_handler.resolve_error(expr.name, "Cannot read local variable in its own initializer.")
    self.__resolve_local(expr, expr.name)

  def visitAssignExpr(self, expr):
    self.__resolve(expr.value)
    self.__resolve_local(expr, expr.name)

  def visitClassStmt(self, stmt):
    self.__declare(stmt.name)
    self.__define(stmt.name)
    for method in stmt.methods:
      self.__resolve_function(method, FunctionType.METHOD)
    
  def visitFunctionStmt(self, stmt):
    self.__declare(stmt.name)
    self.__define(stmt.name)
    self.__resolve_function(stmt, FunctionType.FUNCTION)

  def visitExpressionStmt(self, stmt):
    self.__resolve(stmt.expression)

  def visitIfStmt(self, stmt):
    self.__resolve(stmt.condition)
    self.__resolve(stmt.thenBranch)
    if stmt.elseBranch:
      self.__resolve(stmt.elseBranch)
  
  def visitPrintStmt(self, stmt):
    self.__resolve(stmt.expression)

  def visitReturnStmt(self, stmt):
    if self.current_function == FunctionType.NONE:
      error_handler.resolve_error(stmt.keyword, "Cannot return from top-level code.")
    if stmt.value:
      self.__resolve(stmt.value)

  def visitWhileStmt(self, stmt):
    self.__resolve(stmt.condition)
    self.__resolve(stmt.body)

  def visitBinaryExpr(self, expr):
    self.__resolve(expr.left)
    self.__resolve(expr.right)

  def visitCallExpr(self, expr):
    self.__resolve(expr.callee)
    for argument in expr.arguments:
      self.__resolve(argument)
  
  def visitGetExpr(self, expr):
    self.__resolve(expr.object)

  def visitGroupingExpr(self, expr):
    self.__resolve(expr.expression)

  def visitLiteralExpr(self, expr):
    pass

  def visitLogicalExpr(self, expr):
    self.__resolve(expr.left)
    self.__resolve(expr.right)

  def visitSetExpr(self, expr):
    self.__resolve(expr.value)
    self.__resolve(expr.object)

  def visitUnaryExpr(self, expr):
    self.__resolve(expr.right)

  def __resolve_function(self, func_stmt, func_type):
    enclosing_function = self.current_function
    self.current_function = func_type
    self.__begin_scope()
    for param in func_stmt.params:
      self.__declare(param)
      self.__define(param)
    self.__resolve(func_stmt.body)
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