from typing import List
from unittest import TestCase
from pylox.scanner import Scanner
from pylox.parser import Parser
from pylox.ast_printer import AstPrinter
from pylox.interpreter import Interpreter

class TestInterpreter(TestCase):
      
  def test_interpret_stmts(self):
    stmts = Parser(Scanner("var a=1;var b=2;print a+b;").scan_tokens()).parse()
    Interpreter().interprete(stmts)

  def test_interpret_assign_stmt(self):
    stmts = Parser(Scanner("var a=1;a=2;print a;").scan_tokens()).parse()
    Interpreter().interprete(stmts)

  def test_interpret_scopes(self):
    with open("tests/data/interpreter/scope.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      Interpreter().interprete(stmts)

  def test_interpret_while_stmt(self):
    with open("tests/data/interpreter/while.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      Interpreter().interprete(stmts)

  def test_interpret_for_stmt(self):
    with open("tests/data/interpreter/for.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      Interpreter().interprete(stmts)

  def test_interpret_function_stmt(self):
    with open("tests/data/interpreter/function.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      Interpreter().interprete(stmts)