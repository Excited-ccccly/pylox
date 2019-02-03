class ErrorHandler(object):
  def __init__(self):
    self.had_error = False

  def error(self, line: int, where: str = None, message: str = None):
    print(f"[line{line}] Error. {where}: {message}")
    self.had_error = True

error_handler = ErrorHandler()

class ParseError(Exception):
  pass

class RuntimeError(Exception):
  pass