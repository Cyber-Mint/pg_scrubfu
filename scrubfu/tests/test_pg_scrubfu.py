from unittest import TestCase
from scrubfu.pg_scrubfu import main
from io import StringIO
from contextlib import redirect_stdout


class Test_pg_scrubfu(TestCase):
    def test_pg_scrubfu(self):
        f = StringIO()

        with redirect_stdout(f):
            main()

        self.assertTrue(isinstance(f.getvalue(), str))
