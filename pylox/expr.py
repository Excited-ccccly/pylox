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
  def visit_assign_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_binary_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_call_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_get_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_grouping_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_literal_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_logical_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_set_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_super_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_this_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_unary_expr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_variable_expr(self, expr):
    raise NotImplementedError()
