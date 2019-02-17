from tests.test_base import LoxTestBase
from pylox.cli import main, interpreter
from click.testing import CliRunner
class TestCLI(LoxTestBase):

  def test_execute_a_file(self):
    runner = CliRunner()
    result = runner.invoke(main, "tests/data/interpreter/visitor_pattern_in_lox.lox")
    # self.assertEqual(0, result.exit_code)
    # self.assertEqual("a=1\n", result.output)
    interpreter.__init__()

  def test_execute_repl(self):
    runner = CliRunner()
    result = runner.invoke(main, input="var a=1;print a;\n\n")
    # self.assertEqual(1, result.exit_code)
    # self.assertEqual("> 1.0", result.output.splitlines()[0])
    interpreter.__init__()

