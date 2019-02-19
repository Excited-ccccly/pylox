from inspect import Parameter, Signature

def make_signature(names):
  return Signature(
    Parameter(name,
      Parameter.POSITIONAL_OR_KEYWORD)
    for name in names
  )

def add_signature(*names):
  """decorator for adding parameter signature for class
  """
  def decorate(cls):
    cls.__signature__ = make_signature(names)
    return cls
  return decorate

class ExprMeta(type):
  """metaclass for expr classes
  """
  def __new__(cls, name, bases, clsdict):
    clsobj = super().__new__(cls, name, bases, clsdict)
    def accept(self, vistor):
      visit_callable = getattr(vistor, f"visit_{name.lower()}_expr")
      return visit_callable(self)
    setattr(clsobj, "accept", accept)
    return clsobj

class StmtMeta(type):
  """metaclass for stmt classes
  """
  def __new__(cls, name, bases, clsdict):
    clsobj = super().__new__(cls, name, bases, clsdict)
    def accept(self, vistor):
      visit_callable = getattr(vistor, f"visit_{name.lower()}_stmt")
      return visit_callable(self)
    setattr(clsobj, "accept", accept)
    return clsobj