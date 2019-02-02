from pylox.meta import ExprMeta, make_signature, add_signature

class Expr(metaclass=ExprMeta):
  __signature__ = make_signature([])

  def __init__(self, *args, **kwargs):
    bound = self.__signature__.bind(*args, **kwargs)
    for name, val in bound.arguments.items():
      setattr(self, name, val)

@add_signature('name', 'value')
class Assign(Expr):
  pass

@add_signature('left', 'operator', 'right')
class Binary(Expr):
  pass

@add_signature('callee', 'paren', 'arguments')
class Call(Expr):
  pass

@add_signature('object', 'name')
class Get(Expr):
  pass

@add_signature('expression')
class Grouping(Expr):
  pass

@add_signature('value')
class Literal(Expr):
  pass

@add_signature('left', 'operator', 'right')
class Logical(Expr):
  pass

@add_signature('keyword', 'method')
class Super(Expr):
  pass

@add_signature('object', 'name', 'value')
class Set(Expr):
  pass

@add_signature('keyword')
class This(Expr):
  pass

@add_signature('operator', 'right')
class Unary(Expr):
  pass

@add_signature('name')
class Variable(Expr):
  pass

from abc import abstractmethod

class ExprVisitor:
  @abstractmethod
  def visitAssignExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitBinaryExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitCallExpr(self, expr):
    raise NotImplementedError()    
  @abstractmethod
  def visitGetExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitGroupingExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitLiteralExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitLogicalExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitSetExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitSuperExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitThisExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitUnaryExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitVariableExpr(self, expr):
    raise NotImplementedError()    
