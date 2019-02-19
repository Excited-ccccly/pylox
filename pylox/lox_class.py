from pylox.lox_callable import LoxCallable
from pylox.token import Token

class LoxClass(LoxCallable):

  def __init__(self, name:str, superclass, methods):
    self.name = name
    self.methods = methods
    self.superclass = superclass

  def arity(self):
    """constructor arity
    """
    initializer = self.methods.get("init")
    if initializer:
      return initializer.arity()
    return 0

  def call(self, interpreter, arguments):
    """call constructor
    """
    instance = LoxInstance(self)
    initializer = self.methods.get("init")
    if initializer:
      initializer.bind(instance).call(interpreter, arguments)
    return instance

  def find_method(self, instance, name: str):
    """method can be in this class or super class.
    """
    if self.methods.__contains__(name):
      return self.methods[name].bind(instance)
    if self.superclass:
      return self.superclass.find_method(instance, name)

  def __repr__(self):
    return self.name

class LoxInstance:

  def __init__(self, klass):
    self.klass = klass
    self.fields = {}

  def get(self, token: Token):
    """get field or method
    """
    if self.fields.__contains__(token.lexeme):
      return self.fields[token.lexeme]
    method = self.klass.find_method(self, token.lexeme)
    if method: return method
    raise RuntimeError(f'Undefined property: {token.lexeme}')

  def set(self, name: str, value):
    """set field or method
    """
    self.fields[name] = value

  def __repr__(self):
    return f"{self.klass} Instance"
