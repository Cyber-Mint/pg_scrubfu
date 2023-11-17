
import re
import sys
import logging

class ColumnCommentValidator:
    def __init__(self, comment):
        self.comment = comment
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        #Standard output
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)

        #Standard error
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)
        stderr_handler.setFormatter(formatter)
        self.logger.addHandler(stderr_handler)

    def validate(self):
        # Check if the comment starts and ends with tildes (~)
        if not self.comment.startswith("~") or not self.comment.endswith("~"):
            self.logger.error("Invalid comment format. It should be enclosed in tildes (~).")
            return False

        # Extract the content between tildes for validation
        comment_content = self.comment[1:-1]

        # Check if multiple script-tags are present and follow the specified format
        script_tags = comment_content.split('~')
        for script in script_tags:
            if script.strip() and not self.is_valid_script_tag(script.strip()):
                self.logger.error(f"Invalid script-tag format: {script}")
                return False

        self.logger.info("Comment is valid.")
        return True

    def is_valid_script_tag(self, script):
        # Validate the format and parameters of each script-tag
        script_pattern = re.compile(r'^([a-zA-Z]+:)?(MASK|REPLACE|RANDOM|LIST|DROP|MA|RE|RA|LI|DR):[a-zA-Z0-9]+((\d+))?$')
        if not script_pattern.match(script):
            return False

        # Checks if there is a colon(:) after the script-tag
        parts = script.split(':', 1)
        if len(parts) == 2:
            definition = parts[0].strip()
            tag, params = parts[1].split(':', 1) if ':' in parts[1] else (parts[1], '')
        else:
            tag, params = parts[0].split(':', 1) if ':' in parts[0] else (parts[0], '')

         # Checks for valid script-tags and aliases
        valid_tags = {'MASK', 'REPLACE', 'RANDOM', 'LIST', 'DROP', 'MA', 'RE', 'RA', 'LI', 'DR'}
        if tag not in valid_tags:
            return True


#Example for testing:
comment = "~MASK:email~"
validator = ColumnCommentValidator(comment)
validator.validate()