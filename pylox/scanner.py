from typing import List
from pylox.token import Token, TokenType, lexeme_token_type_dict
from pylox.error import error_handler

class Scanner(object):
  """scan source code to get a list of tokens
  """

  def __init__(self, source: str):
    """
    :param source: source code str
    """
    self.source = source
    self.source_length = len(self.source)
    self.tokens = []
    self.start = 0
    self.current = 0
    self.line = 1

  def scan_tokens(self) -> List[Token]:
    """Lexing
    """
    while not self.is_at_end():
      self.start = self.current
      self.scan_token()
      self.advance()
    self.tokens.append(Token(TokenType.EOF, "", None, self.line))
    return self.tokens

  def is_at_end(self):
    return self.current >= self.source_length

  def scan_token(self):
    """Parse one token and add it into tokens. Notice that here is a different
       way to parse token from the official Java implementation.
    """
    c = self.peek()
    if c in ("!", "=", "<", ">"):
      if self.look_ahead() == "=":
        self.advance()
        self.add_token(lexeme_token_type_dict[c+self.peek()])
      else:
        self.add_token(lexeme_token_type_dict[c])
    elif c == "/":
      if self.look_ahead() == "/":
        while self.look_ahead() != "\n" and not self.is_at_end():
          self.advance()
      else:
        self.add_token(lexeme_token_type_dict[c])
    elif c in (" ", "\r", "\t"):
      return
    elif c == "\n":
      self.line += 1
    elif c in ('"', '\''):
      while self.look_ahead() not in ('"', '\'') and not self.is_at_end():
        if self.look_ahead() == "\n": self.line += 1
        self.advance()
      if self.is_at_end():
        error_handler.error(self.line, message="Unterminated string.")
        return
      self.advance()
      str_value = self.source[self.start+1: self.current]
      self.add_token(TokenType.STRING, str_value)
    elif c.isdigit():
      while self.look_ahead().isdigit(): self.advance()
      if self.look_ahead() == "." and self.look_ahead2().isdigit():
        self.advance()
        while self.look_ahead().isdigit(): self.advance()
      self.add_token(TokenType.NUMBER, literal=float(self.source[self.start:self.current+1]))
    elif c.isalpha() or c == "_":
      while self.look_ahead().isalnum(): self.advance()
      value = self.source[self.start:self.current+1]
      if lexeme_token_type_dict.__contains__(value):
        self.add_token(lexeme_token_type_dict[value])
      else:
        self.add_token(TokenType.IDENTIFIER)
    elif lexeme_token_type_dict.__contains__(c):
      self.add_token(lexeme_token_type_dict[c])
    else:
      error_handler.error(self.line, message="Unexpected character")


  def look_ahead(self) -> str:
    """Look next char
    """
    if self.current + 1 >= self.source_length: return "\0"
    return self.source[self.current + 1]

  def look_ahead2(self) -> str:
    """Look the second char following current char
    """
    if self.current + 2 >= self.source_length: return "\0"
    return self.source[self.current + 2]

  def peek(self) -> str:
    """Look current char
    """
    return self.source[self.current]

  def advance(self):
    """Move the cursor to next char
    """
    self.current += 1

  def add_token(self, token_type: TokenType, literal=None):
    """Add token into tokens
    :param token_type: token's type, a enum
    :param literal: literal value of the token. Only present if
        token is number, string
    """
    text: str = self.source[self.start:self.current+1]
    self.tokens.append(Token(token_type, text, literal, self.line))