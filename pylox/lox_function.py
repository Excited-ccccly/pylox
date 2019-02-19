from pylox.lox_callable import LoxCallable
from pylox.environment import Environment
from pylox.error import ReturnValue

class LoxFunction(LoxCallable):

  def __init__(self, func_declaration, closure, is_initializer):
    self.declaration = func_declaration
    self.closure = closure
    self.is_initializer = is_initializer

  def call(self, interpreter, arguments):
    """create environment dynamicly for each function call.
    """
    environment = Environment(self.closure)
    for param, argument in zip(self.declaration.params, arguments):
      environment.define(param.name.lexeme, argument)
    try:
      interpreter.execute_block(self.declaration.body.statements, environment)
    except ReturnValue as r:
      # initializer always return this
      if self.is_initializer:
        return self.closure.get_at(0, "this")
      return r.value
    if self.is_initializer:
      return self.closure.get_at(0, "this")

  def bind(self, instance):
    """bind current function to a specific instance.
    define this keyword in parent environment.
    """
    environment = Environment(self.closure)
    environment.define("this", instance)
    return LoxFunction(self.declaration, environment, self.is_initializer)

  def arity(self):
    """function's arguments count.
    """
    return len(self.declaration.params)

  def __repr__(self):
    return f"<fn {self.declaration.name.lexeme}>"
