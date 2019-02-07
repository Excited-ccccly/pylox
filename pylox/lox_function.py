from pylox.lox_callable import LoxCallable
from pylox.environment import Environment
from pylox.error import ReturnValue

class LoxFunction(LoxCallable):

  def __init__(self, func_declaration, closure):
    self.declaration = func_declaration
    self.closure = closure

  def call(self, interpreter, arguments):
    environment = Environment(self.closure)
    for param, argument in zip(self.declaration.params, arguments):
      environment.define(param.name.lexeme, argument)
    try:
      interpreter.execute_block(self.declaration.body.statements, environment)
    except ReturnValue as r:
      return r.value

  def arity(self):
    return len(self.declaration.params)

  def __repr__(self):
    return f"<fn {self.declaration.name.lexeme}>"
