from typing import List
from pylox.token import Token, TokenType
from pylox.expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign, Logical, Call
from pylox.stmt import Print, Expression, Var, Block, If, While, Function, Return
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
      if self.__match(TokenType.FUN): return self.__fun_delcaration()
      return self.__stmt()
    except ParseError:
      self.__synchronize()

  def __fun_delcaration(self):
    self.__advance()
    return self.__function()

  def __function(self):
    name: Token = self.__consume(TokenType.IDENTIFIER, err_msg="Expect function name")
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after function name")
    params = []
    if not self.__match(TokenType.RIGHT_PAREN):
      params.append(self.__primary())
      while self.__match_then_advance(TokenType.COMMA):
        if len(params) >= 8:
          error_handler.parse_error(self.__peek(), "Cannot have more than 8 parameters.")
        params.append(self.__primary())
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters")
    body = self.__block()
    return Function(name, params, body)

  def __var_declaration(self):
    self.__advance()
    name: Token = self.__consume(TokenType.IDENTIFIER, err_msg="Expect variable name")
    initializer: Expr = None
    if self.__match_then_advance(TokenType.EQUAL):
      initializer = self.__expression()
    self.__consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
    return Var(name=name, initializer=initializer)
    
  def __stmt(self):
    if self.__match(TokenType.LEFT_BRACE): return self.__block()
    if self.__match(TokenType.FOR): return self.__for_stmt()
    if self.__match(TokenType.IF): return self.__if_stmt()
    if self.__match(TokenType.PRINT): return self.__print_stmt()
    if self.__match(TokenType.RETURN): return self.__return_stmt()
    if self.__match(TokenType.WHILE): return self.__while_stmt()
    return self.__expr_stmt()
  
  def __block(self):
    self.__advance()
    stmts = []
    while not self.__match(TokenType.RIGHT_BRACE) and not self.__is_at_end():
      stmts.append(self.__declaration())
    self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
    return Block(statements=stmts)

  def __expr_stmt(self):
    expr = self.__expression()
    self.__consume(expected=TokenType.SEMICOLON, err_msg="Expect ';' after statement.")
    return Expression(expr)

  def __for_stmt(self):
    self.__advance()
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
    initializer = None
    if self.__match(TokenType.VAR):
      initializer = self.__declaration()
    elif not self.__match_then_advance(TokenType.SEMICOLON):
      self.__expr_stmt()
      self.__advance()
    condition = None
    if not self.__match_then_advance(TokenType.SEMICOLON):
      condition = self.__expression()
      self.__advance()
    increment = None
    if not self.__match_then_advance(TokenType.RIGHT_PAREN):
      increment = self.__expression()
      self.__advance()
    body = self.__stmt()
    if increment:
      body = Block(statements=[body, increment])
    if not condition:
      condition = Literal(True)
    body = While(condition, body)
    if initializer:
      body = Block(statements=[initializer, body])
    return body    
  
  def __if_stmt(self):
    self.__advance()
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
    condition = self.__expression()
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
    then_branch = self.__stmt()
    else_branch = None
    if self.__match_then_advance(TokenType.ELSE):
      else_branch = self.__stmt()
    return If(condition, then_branch, else_branch)

  def __print_stmt(self):
    self.__advance()
    expr = self.__expression()
    self.__consume(expected=TokenType.SEMICOLON, err_msg="Expect ';' after statement.")
    return Print(expr)    

  def __return_stmt(self):
    keyword = self.__peek()
    self.__advance()
    return_value = None
    if self.__match_then_advance(TokenType.SEMICOLON):
      return return_value
    else:
      return_value = self.__expression()
      self.__consume(TokenType.SEMICOLON, "Expect ';' after return value.")
    return Return(keyword, return_value)

  def __while_stmt(self):
    self.__advance()
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
    condition = self.__expression()
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
    body = self.__stmt()
    return While(condition, body)
      
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
    return self.__call()

  def __call(self) -> Expr:
    expr = self.__primary()
    while True:
      if self.__match_then_advance(TokenType.LEFT_PAREN):
        expr = self.__finish_call(expr)
      else:
        break
    return expr

  def __finish_call(self, callee):
    arguments = []
    if not self.__match(TokenType.RIGHT_PAREN):
      arguments.append(self.__expression())
      while self.__match_then_advance(TokenType.COMMA):
        if len(arguments) >= 8:
          error_handler.parse_error(self.__peek(), "Cannot have more than 8 arguments.")
        arguments.append(self.__expression())
    paren = self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
    return Call(callee, paren, arguments)


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
      error_handler.parse_error(self.__peek(), err_msg)
      raise ParseError(err_msg)    
  
  def __check(self, token_type: TokenType) -> bool:
    if self.__is_at_end(): return False
    return self.__peek().type == token_type

  def __is_at_end(self) -> bool:
    return self.__peek().type == TokenType.EOF

  def __peek(self) -> Token:
    return self.tokens[self.current]

  def __lookahead(self) -> Token:
    return self.tokens[self.current + 1]

  def __advance(self):
    if not self.__is_at_end():
      self.current += 1