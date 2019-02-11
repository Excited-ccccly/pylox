from pylox.lox_callable import LoxCallable
from pylox.token import Token

class LoxClass(LoxCallable):

  def __init__(self, name:str):
    self.name = name

  def arity(self):
    return 0    

  def call(self, interpreter, arguments):
    instance = LoxInstance(self)
    return instance

  def __repr__(self):
    return self.name

class LoxInstance:

  def __init__(self, klass):
    self.klass = klass
    self.fields = {}

  def get(self, token: Token):
    if self.fields.__contains__(token.lexeme):
      return self.fields[token.lexeme]
    raise RuntimeError(f'Undefined property: {token.lexeme}')

  def set(self, name: str, value):
    self.fields[name] = value

  def __repr__(self):
    return f"{self.klass} Instance"
