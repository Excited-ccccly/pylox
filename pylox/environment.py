from pylox.error import RuntimeError
from pylox.token import Token
class Environment:
  def __init__(self):
    self.values = {}

  def define(self, name: str, value):
    self.values[name] = value

  def get(self, name: Token):
    if self.values.__contains__(name.lexeme):
      return self.values[name.lexeme]
    raise RuntimeError(f'Undefined variable: {name.lexeme}')
