from pylox.error import RuntimeError
from pylox.token import Token

class Environment:
  def __init__(self, enclosing = None):
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

  def get_at(self, distance, token: Token):
    return self.__ancestor(distance).values.get(token)

  def assign_at(self, distance, name: str, value):
    self.__ancestor(distance).values[name] = value

  def __ancestor(self, distance):
    environment = self
    for i in range(0, distance):
      environment = environment.enclosing
    return environment

