from pylox.error import RuntimeError
from pylox.token import Token

class Environment:
  def __init__(self, enclosing = None):
    self.values = {}
    self.enclosing: Environment = enclosing

  def define(self, name: str, value):
    self.values[name] = value

  def assign(self, name: str, value):
    """assign value to a variable in this environment or parent environment
    """
    if self.values.__contains__(name):
      self.values[name] = value
      return
    if self.enclosing:
      return self.enclosing.assign(name, value)
    raise RuntimeError(f'Undefined variable: {name}')

  def get(self, token: Token):
    """value can be in this environment or enclosing environment
    """
    if self.values.__contains__(token.lexeme):
      return self.values[token.lexeme]
    if self.enclosing:
      return self.enclosing.get(token)
    raise RuntimeError(f'Undefined variable: {token.lexeme}')

  def get_at(self, distance, token: Token):
    """use distance(hops count) to get variable's value.
    """
    return self.__ancestor(distance).values.get(token)

  def assign_at(self, distance, name: str, value):
    """assign a value to a variable in the specific antecedent environment by distance(hops count)
    """
    self.__ancestor(distance).values[name] = value

  def __ancestor(self, distance):
    """get the specific antecedent environment by distance(hops count)
    """
    environment = self
    for _ in range(0, distance):
      environment = environment.enclosing
    return environment

