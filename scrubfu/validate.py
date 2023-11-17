import re

class ColumnCommentValidator:
    def __init__(self, comment):
        self.comment = comment

    def validate(self):
        # Check if the comment starts and ends with tildes (~)
        if not self.comment.startswith("~") or not self.comment.endswith("~"):
            print("Invalid comment format. It should be enclosed in tildes (~).")
            return False

        # Extract the content between tildes for validation
        comment_content = self.comment[1:-1]

        # Check if multiple script-tag are present and follow the specified format
        script_tags = comment_content.split('~')
        for script in script_tags:
            if script.strip() and not self.is_valid_script_tag(script.strip()):
                print("Invalid script-tag format: {script}")
                return False

        print("Comment is valid.")
        return True

    def is_valid_script_tag(self, script):
        # Validate the format and parameters of each script-tag
        script_pattern = re.compile(r'^([a-zA-Z]+:)?(MASK|REPLACE|RANDOM|LIST|DROP|MA|RE|RA|LI|DR):[a-zA-Z0-9_]+((\d+))?$')
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
comment = "~MASK:email ~REPLACE:12345 ~RANDOM:10~"
validator = ColumnCommentValidator(comment)
validator.validate()