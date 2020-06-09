from unittest import TestCase
from app.app_cli import main
from io import StringIO
from contextlib import redirect_stdout


class Test_app_cli(TestCase):
    def test_cli(self):
        f = StringIO()

        with redirect_stdout(f):
            main()

        self.assertTrue(isinstance(f.getvalue(), str))
