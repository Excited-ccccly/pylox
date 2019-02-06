from abc import abstractmethod
from datetime import datetime

class LoxCallable:
  
  @abstractmethod
  def arity(self):
    raise NotImplementedError()

  @abstractmethod
  def call(self, interpreter, arguments):
    raise NotImplementedError()

class Clock(LoxCallable):
  def arity(self):
    return 0

  def call(self, interpreter, arguments):
    return datetime.now().timestamp()