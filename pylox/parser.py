from typing import List
from pylox.token import Token, TokenType
from pylox.expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign, Logical, Call, Get, Set, This, Super
from pylox.stmt import Print, Expression, Var, Block, If, While, Function, Return, Class
from pylox.error import ParseError, error_handler

class Parser:
  """A recursive descent parser for lox lang
  """

  def __init__(self, tokens: List[Token]):
    self.current = 0
    self.tokens: List[Token] = tokens
    self.token_count = len(tokens)

  def parse(self):
    """
    program        → declaration* EOF ;
    """
    stmts = []
    while not self.__is_at_end():
      stmts.append(self.__declaration())
    return stmts

  def __declaration(self):
    """
    declaration    → classDecl
                  | funDecl
                  | varDecl
                  | statement ;
    """
    try:
      if self.__match(TokenType.VAR): return self.__var_declaration()
      if self.__match(TokenType.FUN): return self.__fun_declaration()
      if self.__match(TokenType.CLASS): return self.__class_declaration()
      return self.__stmt()
    except ParseError:
      self.__synchronize()

  def __class_declaration(self):
    """
    classDecl      → "class" IDENTIFIER ( "<" IDENTIFIER )?
                 "{" function* "}" ;
    """
    self.__advance()
    name: Token = self.__consume(TokenType.IDENTIFIER, "Expect class name.")
    superclass = None
    if self.__match_then_advance(TokenType.LESS):
      superclass_token = self.__consume(TokenType.IDENTIFIER, "Expect superclass name.")
      superclass = Variable(name=superclass_token)
    self.__consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
    methods = []
    while not self.__match_then_advance(TokenType.RIGHT_BRACE) and not self.__is_at_end():
      methods.append(self.__function("method"))
    return Class(name, superclass=superclass, methods=methods)

  def __fun_declaration(self):
    """
    funDecl        → "fun" function ;
    """
    self.__advance()
    return self.__function("function")

  def __function(self, kind: str):
    """
    function       → IDENTIFIER "(" parameters? ")" block ;
    parameters     → IDENTIFIER ( "," IDENTIFIER )* ;
    arguments      → expression ( "," expression )* ;
    """
    name: Token = self.__consume(TokenType.IDENTIFIER, err_msg=f"Expect {kind} name")
    self.__consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name")
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
    """
    varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;
    """
    self.__advance()
    name: Token = self.__consume(TokenType.IDENTIFIER, err_msg="Expect variable name")
    initializer: Expr = None
    if self.__match_then_advance(TokenType.EQUAL):
      initializer = self.__expression()
    self.__consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
    return Var(name=name, initializer=initializer)

  def __stmt(self):
    """
    statement      → exprStmt
                  | forStmt
                  | ifStmt
                  | printStmt
                  | returnStmt
                  | whileStmt
                  | block ;
    """
    if self.__match(TokenType.LEFT_BRACE): return self.__block()
    if self.__match(TokenType.FOR): return self.__for_stmt()
    if self.__match(TokenType.IF): return self.__if_stmt()
    if self.__match(TokenType.PRINT): return self.__print_stmt()
    if self.__match(TokenType.RETURN): return self.__return_stmt()
    if self.__match(TokenType.WHILE): return self.__while_stmt()
    return self.__expr_stmt()

  def __block(self):
    """
    block          → "{" declaration* "}" ;
    """
    self.__advance()
    stmts = []
    while not self.__match(TokenType.RIGHT_BRACE) and not self.__is_at_end():
      stmts.append(self.__declaration())
    self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
    return Block(statements=stmts)

  def __expr_stmt(self):
    """
    exprStmt       → expression ";" ;
    """
    expr = self.__expression()
    self.__consume(expected=TokenType.SEMICOLON, err_msg="Expect ';' after statement.")
    return Expression(expr)

  def __for_stmt(self):
    """ desugar to while statement.

    forStmt        → "for" "(" ( varDecl | exprStmt | ";" )
                           expression? ";"
                           expression? ")" statement ;
    """
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
    """
    ifStmt         → "if" "(" expression ")" statement ( "else" statement )? ;
    """
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
    """
    printStmt      → "print" expression ";" ;
    """
    self.__advance()
    expr = self.__expression()
    self.__consume(expected=TokenType.SEMICOLON, err_msg="Expect ';' after statement.")
    return Print(expr)

  def __return_stmt(self):
    """
    returnStmt     → "return" expression? ";" ;
    """
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
    """
    whileStmt      → "while" "(" expression ")" statement ;
    """
    self.__advance()
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
    condition = self.__expression()
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
    body = self.__stmt()
    return While(condition, body)

  def __expression(self) -> Expr:
    """
    expression     → assignment ;
    """
    return self.__assignment()

  def __assignment(self) -> Expr:
    """
    assignment     → ( call "." )? IDENTIFIER "=" assignment
               | logic_or;
    """
    expr = self.__logic_or()
    if self.__match(TokenType.EQUAL):
      equals: Token = self.__peek()
      self.__advance()
      value: Expr = self.__assignment()
      if isinstance(expr, Variable):
        name: Token = expr.name
        return Assign(name, value)
      elif isinstance(expr, Get):
        return Set(object=expr.object, name=expr.name, value=value)
      error_handler.parse_error(equals, "Invalid assignment target.")
    return expr

  def __logic_or(self) -> Expr:
    """
    logic_or       → logic_and ( "or" logic_and )* ;
    """
    left = self.__logic_and()
    while self.__match(TokenType.OR):
      operator = self.__peek()
      self.__advance()
      right = self.__logic_and()
      left = Logical(left, operator, right)
    return left


  def __logic_and(self) -> Expr:
    """
    logic_and      → equality ( "and" equality )* ;
    """
    left = self.__equality()
    while self.__match(TokenType.AND):
      operator = self.__peek()
      self.__advance()
      right = self.__equality()
      left = Logical(left, operator, right)
    return left

  def __equality(self) -> Expr:
    """
    equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    """
    expr = self.__comparison()
    while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
      operator = self.__peek()
      self.__advance()
      right = self.__comparison()
      expr = Binary(expr, operator, right)
    return expr

  def __comparison(self) -> Expr:
    """
    comparison     → addition ( ( ">" | ">=" | "<" | "<=" ) addition )* ;
    """
    expr =  self.__addition()
    while self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
      operator = self.__peek()
      self.__advance()
      right = self.__addition()
      expr = Binary(expr, operator, right)
    return expr

  def __addition(self) -> Expr:
    """
    addition       → multiplication ( ( "-" | "+" ) multiplication )* ;
    """
    expr =  self.__multiplication()
    while self.__match(TokenType.PLUS, TokenType.MINUS):
      operator = self.__peek()
      self.__advance()
      right = self.__multiplication()
      expr = Binary(expr, operator, right)
    return expr

  def __multiplication(self) -> Expr:
    """
    multiplication → unary ( ( "/" | "*" ) unary )* ;
    """
    expr =  self.__unary()
    while self.__match(TokenType.SLASH, TokenType.STAR):
      operator = self.__peek()
      self.__advance()
      right = self.__unary()
      expr = Binary(expr, operator, right)
    return expr

  def __unary(self) -> Expr:
    """
    unary          → ( "!" | "-" ) unary | call ;
    """
    if self.__match(TokenType.BANG, TokenType.MINUS):
      operator = self.__peek()
      self.__advance()
      right = self.__unary()
      return Unary(operator, right)
    return self.__call()

  def __call(self) -> Expr:
    """
    call           → primary ( "(" arguments? ")" | "." IDENTIFIER )* ;
    """
    expr = self.__primary()
    while True:
      if self.__match_then_advance(TokenType.LEFT_PAREN):
        expr = self.__finish_call(expr)
      elif self.__match_then_advance(TokenType.DOT):
        name = self.__consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
        expr = Get(expr, name)
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
    """
    primary        → "true" | "false" | "nil" | "this"
               | NUMBER | STRING | IDENTIFIER | "(" expression ")"
               | "super" "." IDENTIFIER ;
    """
    if self.__match_then_advance(TokenType.TRUE):
      return Literal(True)
    if self.__match_then_advance(TokenType.FALSE):
      return Literal(False)
    if self.__match_then_advance(TokenType.NIL):
      return Literal(None)
    if self.__match(TokenType.SUPER):
      token = self.__peek()
      self.__advance()
      self.__consume(TokenType.DOT, "Expect '.' after 'super'.")
      method = self.__consume(TokenType.IDENTIFIER, "Expect superclass method name.")
      return Super(keyword=token, method=method)
    if self.__match(TokenType.THIS):
      token = self.__peek()
      self.__advance()
      return This(keyword=token)
    if self.__match(TokenType.STRING, TokenType.NUMBER):
      value = self.__peek().literal
      self.__advance()
      return Literal(value)
    if self.__match_then_advance(TokenType.LEFT_PAREN):
      expr = self.__expression()
      self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
      return Grouping(expr)
    if self.__match(TokenType.IDENTIFIER):
      variable = self.__peek()
      self.__advance()
      return Variable(name=variable)

  def __synchronize(self):
    """ synchronize parser to next statement to recover from panic(error) mode.
    """
    while not self.__is_at_end():
      if self.__match_then_advance(TokenType.SEMICOLON):
        return
      if self.__match(TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR,
                      TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN):
        return
      self.__advance()

  def __match(self, *types) -> bool:
    """check whether current token match expected Token types
    """
    return any([self.__check(t) for t in types])

  def __match_then_advance(self, *types) -> bool:
    """check whether current token match expected Token types. advance if match.
    """
    if self.__match(*types):
      self.__advance()
      return True
    return False

  def __consume(self, expected: TokenType, err_msg: str):
    """consume expected TokenType, raise a ParseError otherwise.
    """
    if self.__match(expected):
      token = self.__peek()
      self.__advance()
      return token
    else:
      error_handler.parse_error(self.__peek(), err_msg)
      raise ParseError(err_msg)

  def __check(self, token_type: TokenType) -> bool:
    """check exactly TokenType
    """
    if self.__is_at_end(): return False
    return self.__peek().type == token_type

  def __is_at_end(self) -> bool:
    """check whether current token is at the end of source code.
    """
    return self.__peek().type == TokenType.EOF

  def __peek(self) -> Token:
    """return current token
    """
    return self.tokens[self.current]

  def __lookahead(self) -> Token:
    """lookahead one token
    """
    return self.tokens[self.current + 1]

  def __advance(self):
    """move to next token
    """
    if not self.__is_at_end():
      self.current += 1