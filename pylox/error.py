from pylox.token import Token, TokenType
class ErrorHandler(object):
  def __init__(self):
    self.had_error = False

  def error(self, line: int, where: str = None, message: str = None):
    print(f"[line{line}] Error. {where}: {message}")
    self.had_error = True

  def parse_error(self, token: Token, message: str):
    if token.type == TokenType.EOF:
      self.error(token.line, " at end", message)
    else:
      self.error(token.line, f" at '{token.lexeme}'", message)

error_handler = ErrorHandler()

class ParseError(Exception):
  pass

class RuntimeError(Exception):
  pass

class ReturnValue(Exception):
  def __init__(self, value):
    self.value = value  