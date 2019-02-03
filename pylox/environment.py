from pylox.error import RuntimeError
from pylox.token import Token
class Environment:
  def __init__(self):
    self.values = {}

  def define(self, name: str, value):
    self.values[name] = value

  def assign(self, name: str, value):
    if self.values.__contains__(name):
      self.values[name] = value
      return
    raise RuntimeError(f'Undefined variable: {name}')      

  def get(self, token: Token):
    if self.values.__contains__(token.lexeme):
      return self.values[token.lexeme]
    raise RuntimeError(f'Undefined variable: {token.lexeme}')
