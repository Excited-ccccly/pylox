from typing import List
from unittest import TestCase
from pylox.scanner import Scanner
from pylox.parser import Parser
from pylox.ast_printer import AstPrinter
from pylox.interpreter import Interpreter

class TestInterpreter(TestCase):
      
  def test_stmts_interpret(self):
    stmts = Parser(Scanner("var a=1;var b=2;print a+b;").scan_tokens()).parse()
    Interpreter().interprete(stmts)

  def test_assign_interpret(self):
    stmts = Parser(Scanner("var a=1;a=2;print a;").scan_tokens()).parse()
    Interpreter().interprete(stmts)

  def test_scopes(self):
    with open("tests/data/test_interpreter.lox") as f:
      stmts = Parser(Scanner(f.read()).scan_tokens()).parse()
      Interpreter().interprete(stmts)