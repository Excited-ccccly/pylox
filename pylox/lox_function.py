from pylox.lox_callable import LoxCallable
from pylox.environment import Environment

class LoxFunction(LoxCallable):

  def __init__(self, func_declaration):
    self.declaration = func_declaration

  def call(self, interpreter, arguments):
    environment = Environment(interpreter.globals)
    for param, argument in zip(self.declaration.params, arguments):
      environment.define(param.name.lexeme, argument)
    interpreter.execute_block(self.declaration.body.statements, environment)

  def arity(self):
    return len(self.declaration.params)

  def __repr__(self):
    return f"<fn {self.declaration.name.lexeme}>"
