from abc import abstractmethod

class ExprVisitor:
  @abstractmethod
  def visitAssignExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitBinaryExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitCallExpr(self, expr):
    raise NotImplementedError()    
  @abstractmethod
  def visitGetExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitGroupingExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitLiteralExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitLogicalExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitSetExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitSuperExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitThisExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitUnaryExpr(self, expr):
    raise NotImplementedError()
  @abstractmethod
  def visitVariableExpr(self, expr):
    raise NotImplementedError()    
