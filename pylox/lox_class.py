from pylox.lox_callable import LoxCallable
from pylox.token import Token

class LoxClass(LoxCallable):

  def __init__(self, name:str, methods):
    self.name = name
    self.methods = methods

  def arity(self):
    return 0    

  def call(self, interpreter, arguments):
    instance = LoxInstance(self)
    return instance

  def find_method(self, instance, name):
    if self.methods.__contains__(name):
      return self.methods[name].bind(instance)

  def __repr__(self):
    return self.name

class LoxInstance:

  def __init__(self, klass):
    self.klass = klass
    self.fields = {}

  def get(self, token: Token):
    if self.fields.__contains__(token.lexeme):
      return self.fields[token.lexeme]
    method = self.klass.find_method(self, token.lexeme)
    if method: return method
    raise RuntimeError(f'Undefined property: {token.lexeme}')

  def set(self, name: str, value):
    self.fields[name] = value

  def __repr__(self):
    return f"{self.klass} Instance"
