from typing import List
from tests.test_base import LoxTestBase
from pylox.scanner import Scanner
from pylox.parser import Parser
from pylox.ast_printer import AstPrinter
from pylox.interpreter import Interpreter
from pylox.resolver import Resolver

class TestInterpreter(LoxTestBase):

  def test_interpret_stmts(self):
    stmts = Parser(Scanner("var a=1;var b=2;print a+b;").scan_tokens()).parse()
    interpreter = Interpreter()
    Resolver(interpreter).resolve(stmts)
    with self.assertStdout() as output:
      interpreter.interprete(stmts)
      self.assertEqual("3.0\n", output.getvalue())

  def test_interpret_assign_stmt(self):
    stmts = Parser(Scanner("var a=1;a=2;print a;").scan_tokens()).parse()
    interpreter = Interpreter()
    Resolver(interpreter).resolve(stmts)
    with self.assertStdout() as output:
      interpreter.interprete(stmts)
      self.assertEqual("2.0\n", output.getvalue())

  def test_interpret_scopes(self):
    with open("tests/data/interpreter/scope.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      interpreter = Interpreter()
      Resolver(interpreter).resolve(stmts)
      with self.assertStdout() as output:
        interpreter.interprete(stmts)
        self.assertEqual("inner a\nouter b\nglobal c\nouter a\nouter b\nglobal c\nglobal a\nglobal b\nglobal c\n", output.getvalue())

  def test_interpret_while_stmt(self):
    with open("tests/data/interpreter/while.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      interpreter = Interpreter()
      Resolver(interpreter).resolve(stmts)
      with self.assertStdout() as output:
        interpreter.interprete(stmts)
        self.assertEqual("0.0\n1.0\n1.0\n2.0\n3.0\n5.0\n8.0\n", output.getvalue())

  def test_interpret_for_stmt(self):
    with open("tests/data/interpreter/for.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      interpreter = Interpreter()
      Resolver(interpreter).resolve(stmts)
      with self.assertStdout() as output:
        interpreter.interprete(stmts)
        self.assertEqual("0.0\n1.0\n2.0\n3.0\n4.0\n", output.getvalue())

  def test_interpret_function_stmt(self):
    with open("tests/data/interpreter/function.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      interpreter = Interpreter()
      Resolver(interpreter).resolve(stmts)
      with self.assertStdout() as output:
        interpreter.interprete(stmts)
        self.assertEqual("Hi, Dear Reader!\n", output.getvalue())

  def test_interpret_recursive_fibonacci(self):
    with open("tests/data/interpreter/fibonacci.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      interpreter = Interpreter()
      Resolver(interpreter).resolve(stmts)
      with self.assertStdout() as output:
        interpreter.interprete(stmts)
        self.assertEqual("0.0\n1.0\n1.0\n2.0\n3.0\n", output.getvalue())

  def test_interpret_closure(self):
    with open("tests/data/interpreter/closure.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      interpreter = Interpreter()
      Resolver(interpreter).resolve(stmts)
      with self.assertStdout() as output:
        interpreter.interprete(stmts)
        self.assertEqual("1.0\n2.0\n", output.getvalue())

  def test_interpret_class(self):
    with open("tests/data/interpreter/class.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      interpreter = Interpreter()
      Resolver(interpreter).resolve(stmts)
      with self.assertStdout() as output:
        interpreter.interprete(stmts)
        self.assertEqual("Thing Instance\n", output.getvalue())

  def test_interpret_class_super(self):
    with open("tests/data/interpreter/super.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      interpreter = Interpreter()
      Resolver(interpreter).resolve(stmts)
      with self.assertStdout() as output:
        interpreter.interprete(stmts)
        self.assertEqual("A method\n", output.getvalue())