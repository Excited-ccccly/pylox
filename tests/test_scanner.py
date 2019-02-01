from typing import List
from unittest import TestCase
from pylox.scanner import Scanner
from pylox.token import Token, TokenType

class TestScanner(TestCase):
  def setUp(self):
    with open("tests/data/test_scanner.lox") as f:
      self.scanner = Scanner(f.read())

  def test_scan_tokens(self):
    tokens: List[Token] = self.scanner.scan_tokens()
    self.assertEqual("a", tokens[0].lexeme)
    self.assertEqual(TokenType.IDENTIFIER, tokens[0].type)
    self.assertEqual("{", tokens[15].lexeme)
    self.assertEqual(";", tokens[117].lexeme)

  def tearDown(self):
    self.scanner = None