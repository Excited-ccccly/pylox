from tests.test_base import LoxTestBase
from pylox.scanner import Scanner
from pylox.parser import Parser
from pylox.resolver import Resolver
from pylox.interpreter import Interpreter

class TestResolver(LoxTestBase):

  def test_resolver(self):
    with open("tests/data/test_resolver.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      interpreter = Interpreter()
      Resolver(interpreter).resolve(stmts)
      with self.assertStdout() as output:
        interpreter.interprete(stmts)
        self.assertEqual('global\nglobal\n', output.getvalue())

  def test_resolver_return_at_global_scope(self):
    stmts = Parser(Scanner("var a=1;var b=2;return a+b;").scan_tokens()).parse()
    interpreter = Interpreter()
    with self.assertStdout() as output:
      Resolver(interpreter).resolve(stmts)
      self.assertEqual('[line1] Error.  at \'return\': Cannot return from top-level code.\n', output.getvalue())
