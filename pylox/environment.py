from pylox.error import RuntimeError
from pylox.token import Token

class Environment:
  def __init__(self, enclosing: Environment = None):
    self.values = {}
    self.enclosing: Environment = enclosing

  def define(self, name: str, value):
    self.values[name] = value

  def assign(self, name: str, value):
    if self.values.__contains__(name):
      self.values[name] = value
      return
    if self.enclosing:
      return self.enclosing.assign(name, value)
    raise RuntimeError(f'Undefined variable: {name}')      

  def get(self, token: Token):
    if self.values.__contains__(token.lexeme):
      return self.values[token.lexeme]
    if self.enclosing:
      return self.enclosing.get(token)
    raise RuntimeError(f'Undefined variable: {token.lexeme}')
