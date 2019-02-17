import sys
import io
from unittest import mock
from unittest import TestCase
from contextlib import contextmanager

class LoxTestBase(TestCase):
  @contextmanager
  def assertStdout(self):
    captured = io.StringIO()
    sys.stdout = captured
    try:
      yield captured
    finally:
      sys.stdout = sys.__stdout__
      captured.close()