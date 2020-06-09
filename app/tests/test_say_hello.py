from unittest import TestCase

import app


class Test_say_hello(TestCase):
    def test_is_string(self):
        s = app.say_hello()
        self.assertTrue(isinstance(s, str))
