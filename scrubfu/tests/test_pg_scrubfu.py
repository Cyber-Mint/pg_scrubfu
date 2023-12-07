from unittest import TestCase
from scrubfu.pg_scrubfu import cli
from io import StringIO
from contextlib import redirect_stdout


class TestPGScrubfu(TestCase):
    def test_pg_scrubfu(self):
        f = StringIO()
        with redirect_stdout(f):
            cli()

        self.assertTrue(isinstance(f.getvalue(), str))
