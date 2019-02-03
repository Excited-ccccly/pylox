from typing import List
from pylox.token import Token, TokenType
from pylox.expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign, Logical
from pylox.stmt import Print, Expression, Var, Block, If
from pylox.error import ParseError, error_handler

class Parser:

  def __init__(self, tokens: List[Token]):
    self.current = 0
    self.tokens: List[Token] = tokens
    self.token_count = len(tokens)

  def parse(self):
    stmts = []
    while not self.__is_at_end():
      stmts.append(self.__declaration())
    return stmts

  def __declaration(self):
    try:
      if self.__match(TokenType.VAR): return self.__var_declaration()
      return self.__stmt()
    except ParseError:
      self.__synchronize()

  def __var_declaration(self):
    self.__advance()
    name: Token = self.__consume(TokenType.IDENTIFIER, err_msg="Expect variable name")
    initializer: Expr = None
    if self.__match_then_advance(TokenType.EQUAL):
      initializer = self.__expression()
    self.__consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
    return Var(name=name, initializer=initializer)
    
  def __stmt(self):
    if self.__match_then_advance(TokenType.PRINT): return self.__print_stmt()
    if self.__match_then_advance(TokenType.LEFT_BRACE): return self.__block()
    if self.__match_then_advance(TokenType.IF): return self.__if_stmt()
    return self.__expr_stmt()

  def __print_stmt(self):
    expr = self.__expression()
    self.__consume(expected=TokenType.SEMICOLON, err_msg="Expect ';' after statement.")
    return Print(expr)
  
  def __block(self):
    stmts = []
    while not self.__match(TokenType.RIGHT_BRACE) and not self.__is_at_end():
      stmts.append(self.__declaration())
    self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
    return Block(statements=stmts)
  
  def __if_stmt(self):
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
    condition = self.__expression()
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
    then_branch = self.__stmt()
    else_branch = None
    if self.__match_then_advance(TokenType.ELSE):
      else_branch = self.__stmt()
    return If(condition, then_branch, else_branch)

  def __expr_stmt(self):
    expr = self.__expression()
    self.__consume(expected=TokenType.SEMICOLON, err_msg="Expect ';' after statement.")
    return Expression(expr)
      
  def __expression(self) -> Expr:
    return self.__assignment()

  def __assignment(self) -> Expr:
    expr = self.__logic_or()
    if self.__match(TokenType.EQUAL):
      equals: Token = self.__peek()
      self.__advance()
      value: Expr = self.__assignment()
      if isinstance(expr, Variable):
        name: Token = expr.name
        return Assign(name, value)
      error_handler.parse_error(equals, "Invalid assignment target.")
    return expr

  def __logic_or(self) -> Expr:
    left = self.__logic_and()
    while self.__match(TokenType.OR):
      operator = self.__peek()
      self.__advance()
      right = self.__logic_and()
      left = Logical(left, operator, right)
    return left


  def __logic_and(self) -> Expr:
    left = self.__equality()
    while self.__match(TokenType.AND):
      operator = self.__peek()
      self.__advance()
      right = self.__equality()
      left = Logical(left, operator, right)
    return left

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
    if self.__match_then_advance(TokenType.TRUE):
      return Literal(True)
    if self.__match_then_advance(TokenType.FALSE):
      return Literal(False)
    if self.__match_then_advance(TokenType.NIL):
      return Literal(None)
    if self.__match(TokenType.STRING, TokenType.NUMBER):
      value = self.__peek().literal
      self.__advance()
      return Literal(value)
    if self.__match(TokenType.LEFT_PAREN):
      expr = self.__expression()
      self.__advance()
      self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
      return Grouping(expr)
    if self.__match(TokenType.IDENTIFIER):
      variable = self.__peek()
      self.__advance()
      return Variable(name=variable)

  def __synchronize(self):
    while self.__is_at_end():
      if self.__match_then_advance(TokenType.SEMICOLON):
        return
      if self.__match(TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR,
                      TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN):
        return
      self.__advance()

  def __match(self, *types) -> bool:
    return any([self.__check(t) for t in types])

  def __match_then_advance(self, *types) -> bool:
    if self.__match(*types):
      self.__advance()
      return True
    return False

  def __consume(self, expected: TokenType, err_msg: str):
    if self.__match(expected):
      token = self.__peek()
      self.__advance()
      return token
    else:
      raise ParseError(err_msg)    
  
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