from typing import List
from pylox.token import Token, TokenType
from pylox.expr import Expr, Binary, Unary, Literal, Grouping
from pylox.stmt import Print, Expression

class Parser:

  class ParseError(Exception):
    pass

  def __init__(self, tokens: List[Token]):
    self.current = 0
    self.tokens: List[Token] = tokens
    self.token_count = len(tokens)

  def parse(self):
    try:
      stmts = []
      while not self.__is_at_end():
        stmts.append(self.__stmt())
      return stmts
    except Parser.ParseError:
      return None

  def __stmt(self):
    if self.__match(TokenType.PRINT): return self.__print_stmt()
    return self.__expr_stmt()

  def __print_stmt(self):
    self.__advance()
    expr = self.__expression()
    self.__consume(expected=TokenType.SEMICOLON, msg="Expect ';' after statement.")
    return Print(expr)

  def __expr_stmt(self):
    expr = self.__expression()
    self.__consume(expected=TokenType.SEMICOLON, msg="Expect ';' after statement.")
    return Expression(expr)
      

  def __consume(self, expected: TokenType, msg: str):
    if self.__match(expected):
      self.__advance()
    else:
      raise Parser.ParseError(msg)    

  def __expression(self) -> Expr:
    return self.__equality()

  def __equality(self) -> Expr:
    expr = self.__comparison()
    while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
      operator = self.__peek()
      self.__advance()
      right = self.__comparison()
      expr = Binary(expr, operator, right)
    return expr

  def __comparison(self) -> Expr:
    expr =  self.__addition()
    while self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
      operator = self.__peek()
      self.__advance()
      right = self.__addition()
      expr = Binary(expr, operator, right)
    return expr

  def __addition(self) -> Expr:
    expr =  self.__multiplication()
    while self.__match(TokenType.PLUS, TokenType.MINUS):
      operator = self.__peek()
      self.__advance()
      right = self.__multiplication()
      expr = Binary(expr, operator, right)
    return expr

  def __multiplication(self) -> Expr:
    expr =  self.__unary()
    while self.__match(TokenType.SLASH, TokenType.STAR):
      operator = self.__peek()
      self.__advance()
      right = self.__unary()
      expr = Binary(expr, operator, right)
    return expr

  def __unary(self) -> Expr:
    if self.__match(TokenType.BANG, TokenType.MINUS):
      operator = self.__peek()
      self.__advance()
      right = self.__unary()
      return Unary(operator, right)
    return self.__primary()

  def __primary(self):
    if self.__match(TokenType.TRUE):
      self.__advance()
      return Literal(True)
    if self.__match(TokenType.FALSE):
      self.__advance()
      return Literal(False)
    if self.__match(TokenType.NIL):
      self.__advance()
      return Literal(None)
    if self.__match(TokenType.STRING, TokenType.NUMBER):
      value = self.__peek().literal
      self.__advance()
      return Literal(value)
    if self.__match(TokenType.LEFT_PAREN):
      expr = self.__expression()
      self.__advance()
      if self.__match(TokenType.RIGHT_PAREN):
        self.__advance()
      else:
        raise Parser.ParseError("Expect ')' after expression.")
      return Grouping(expr)

  def __synchronize(self):
    while self.__is_at_end():
      if self.__match(TokenType.SEMICOLON):
        self.__advance()
        return
      if self.__match(TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR,
                      TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN):
        return
      self.__advance()

  def __match(self, *types) -> bool:
    return any([self.__check(t) for t in types])

  def __check(self, token_type: TokenType) -> bool:
    if self.__is_at_end(): return False
    return self.__peek().type == token_type

  def __is_at_end(self) -> bool:
    return self.__peek().type == TokenType.EOF

  def __peek(self) -> Token:
    return self.tokens[self.current]

  def __previous(self) -> Token:
    return self.tokens[self.current - 1]

  def __lookahead(self) -> Token:
    return self.tokens[self.current + 1]

  def __advance(self):
    if not self.__is_at_end():
      self.current += 1