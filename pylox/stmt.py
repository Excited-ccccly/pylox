from abc import abstractmethod
from pylox.meta import StmtMeta, make_signature, add_signature

class Stmt(metaclass=StmtMeta):
  __signature__ = make_signature([])

  def __init__(self, *args, **kwargs):
    bound = self.__signature__.bind(*args, **kwargs)
    for name, val in bound.arguments.items():
      setattr(self, name, val)

@add_signature('statements')
class Block(Stmt):
  pass

@add_signature('name', 'superclass', 'methods')
class Class(Stmt):
  pass

@add_signature('expression')
class Expression(Stmt):
  pass

@add_signature('name', 'params', 'body')
class Function(Stmt):
  pass

@add_signature('condition', 'thenBranch', 'elseBranch')
class If(Stmt):
  pass

@add_signature('expression')
class Print(Stmt):
  pass

@add_signature('keyword', 'value')
class Return(Stmt):
  pass

@add_signature('name', 'initializer')
class Var(Stmt):
  pass

@add_signature('condition', 'body')
class While(Stmt):
  pass

class StmtVisitor:
  @abstractmethod
  def visit_expression_stmt(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_print_stmt(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_var_stmt(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_block_stmt(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_class_stmt(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_if_stmt(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_while_stmt(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_function_stmt(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visit_return_stmt(self, expr):
    raise NotImplementedError()
