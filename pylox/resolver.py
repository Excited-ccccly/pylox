from typing import List
from pylox.expr import ExprVisitor
from pylox.stmt import StmtVisitor
from pylox.token import Token, TokenType
from pylox.error import error_handler

class Resolver(ExprVisitor, StmtVisitor):

  def __init__(self, interpreter):
    self.interpreter = interpreter
    self.scopes: List[dict] = []

  def visitBlockStmt(self, stmt):
    self.__begin_scope()
    self.__resolve(stmt.statements)
    self.__end_scope()

  def visitVarStmt(self, stmt):
    self.__declare(stmt.name)
    if stmt.initializer:
      self.resolve(stmt.initializer)
    self.__define(stmt.name)

  def visitVariableExpr(self, expr):
    if self.scopes and self.scopes[-1].get(expr.name.lexeme) == False:
      error_handler.resolve_error(expr.name, "Cannot read local variable in its own initializer.")
    self.__resolve_local(expr, expr.name)

  def visitAssignExpr(self, expr):
    self.resolve(expr.value)
    self.__resolve_local(expr, expr.name)

  def visitFunctionStmt(self, stmt):
    self.__declare(stmt.name)
    self.__define(stmt.name)
    self.__resolve_function(stmt)

  def visitExpressionStmt(self, stmt):
    self.resolve(stmt.expression)

  def visitIfStmt(self, stmt):
    self.resolve(stmt.condition)
    self.resolve(stmt.thenBranch)
    if stmt.elseBranch:
      self.resolve(stmt.elseBranch)
  
  def visitPrintStmt(self, stmt):
    self.resolve(stmt.expression)

  def visitReturnStmt(self, stmt):
    if stmt.value:
      self.resolve(stmt.value)

  def visitWhileStmt(self, stmt):
    self.resolve(stmt.condition)
    self.resolve(stmt.body)

  def visitBinaryExpr(self, expr):
    self.resolve(expr.left)
    self.resolve(expr.right)

  def visitCallExpr(self, expr):
    self.resolve(expr.calle)
    for argument in expr.arguments:
      self.resolve(argument)

  def visitGroupingExpr(self, expr):
    self.resolve(expr.expression)

  def visitLiteralExpr(self, expr):
    pass

  def visitLogicalExpr(self, expr):
    self.resolve(expr.left)
    self.resolve(expr.right)

  def visitUnaryExpr(self, expr):
    self.resolve(expr.right)
    
  def __resolve_function(self, func_stmt):
    self.__begin_scope()
    for param in func_stmt.params:
      self.__declare(param)
      self.__define(param)
    self.resolve(func_stmt.body)
    self.__end_scope()

  def __resolve_local(self, expr, token):
    for i in reversed(range(0, len(self.scopes))):
      if self.scopes[i].__contains__(token.lexeme):
        self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
        return

  def __declare(self, name: Token):
    if self.scopes:
      scope = self.scopes[-1]
      scope[name.lexeme] = False

  def __define(self, name: Token):
    if self.scopes:
      scope = self.scopes[-1]
      scope[name.lexeme] = True

  def __begin_scope(self):
    self.scopes.append({})

  def __end_scope(self):
    self.scopes.pop()

  def __resolve(self, stmts):
    for stmt in stmts:
      self.resolve(stmt)

  def resolve(self, stmt_or_expr):
    stmt_or_expr.accept(self)