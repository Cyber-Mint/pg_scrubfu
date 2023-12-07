from unittest import TestCase

import scrubfu


class Test_say_hello(TestCase):
    def test_is_string(self):
        s = scrubfu.say_hello()
        self.assertTrue(isinstance(s, str))
