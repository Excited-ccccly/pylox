from inspect import Parameter, Signature

def make_signature(names):
  return Signature(
    Parameter(name,
      Parameter.POSITIONAL_OR_KEYWORD)
    for name in names
  )
class ExprMeta(type):
  def __new__(cls, name, bases, clsdict):
    clsobj = super().__new__(cls, name, bases, clsdict)
    def accept(self, vistor):
      visit_callable = getattr(vistor, f"visit{name}Expr")
      return visit_callable(self)
    setattr(clsobj, "accept", accept)
    return clsobj

class Expr(metaclass=ExprMeta):
  __signature__ = make_signature([])

  def __init__(self, *args, **kwargs):
    bound = self.__signature__.bind(*args, **kwargs)
    for name, val in bound.arguments.items():
      setattr(self, name, val)

def add_signature(*names):
  def decorate(cls):
    cls.__signature__ = make_signature(names)
    return cls
  return decorate

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
