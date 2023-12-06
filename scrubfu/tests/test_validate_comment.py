import unittest
import logging
import sys
sys.path.insert(0, '/home/yusuf/pg_scrubfu/scrubfu')
from validate import validate_comment

# Set up logging configuration for tests
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


class TestValidateComment(unittest.TestCase):
    def setUp(self):
        # Set up logging configuration for tests
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

    def tearDown(self):
        # Clean up after tests (if needed)
        pass

    def test_valid_comments(self):
        valid_comments = [
            "~MA:3,2,#,'@','.'~",
            "~RE:address,addr;'zone','co.uk'~",
            "~DROP:value1~",
            "~RA:+NNN(NNN) NNN-NNNN~",
            "~LI:file.txt,10,SEQ~",
        ]
        for comment in valid_comments:
            with self.subTest(comment=comment):
                result = validate_comment(comment)
                self.assertTrue(result, f"Expected {comment} to be valid")

    def test_invalid_comments(self):
        invalid_comments = [
            "~MA:invalid,2,#,'@','.'~",  # Invalid first parameter for MASK
            "~DROP:value1,value2,value3~",  # Invalid number of parameters for DROP
            "~LI:file.txt,invalid,RND~",  # Invalid second parameter for LIST
            "~INVALIDTAG:parameter1,parameter2~",
        ]
        for comment in invalid_comments:
            with self.subTest(comment=comment):
                result = validate_comment(comment)
                self.assertFalse(result, f"Expected {comment} to be invalid")

    def test_missing_tildes(self):
        # Test case where comment is missing tildes
        comment = "MA:3,2,#,'@','.'"
        result = validate_comment(comment)
        self.assertFalse(result, "Expected missing tildes to be invalid")

    def test_invalid_script_tag(self):
        # Test case where script tag is not in the allowed list
        comment = "~INVALIDTAG:parameter1,parameter2~"
        result = validate_comment(comment)
        self.assertFalse(result, "Expected invalid script tag to be invalid")

    def test_missing_parameters(self):
        # Test case where parameters are missing after the colon
        comment = "~MA:~"
        result = validate_comment(comment)
        self.assertFalse(result, "Expected missing parameters to be invalid")

    def test_valid_random_parameters(self):
        # Test case for valid parameters for the RANDOM tag
        comment = "~RA:+NNN(NNN) NNN-NNNN~"
        result = validate_comment(comment)
        self.assertTrue(result, "Expected valid RANDOM parameters to be valid")

    def test_valid_list_parameters(self):
        # Test case for valid parameters for the LIST tag
        comment = "~LI:file.txt,10,SEQ~"
        result = validate_comment(comment)
        self.assertTrue(result, "Expected valid LIST parameters to be valid")

    def test_invalid_list_parameters(self):
        # Test case for invalid parameters for the LIST tag
        comment = "~LI:file.txt,invalid,RND~"
        result = validate_comment(comment)
        self.assertFalse(result, "Expected invalid LIST parameters to be invalid")


if __name__ == '__main__':
    unittest.main(exit=False)
