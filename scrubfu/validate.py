import re 
import logging 
import sys
from datetime import datetime

# Set up logging configuration
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

def log_error(message):
    logging.error(message)

def log_info(message):
    logging.info(message)

def validate_comment(comment):
    # Comment must begin and end with tildes (~)
    if not comment.startswith("~") or not comment.endswith("~"):
        log_error("Comment does not begin and end with tildes (~)")
        return False
    
    # Comment must have a valid script tag
    script_tags = ['MASK', 'REPLACE', 'LIST', 'DROP', 'RANDOM', 'MA', 'RE', 'LI', 'DR', 'RA']
    match = re.match(r'~([A-Z]+):', comment)
    if not match or match.group(1) not in script_tags:
        log_error("Invalid script tag or missing script tag")
        return False
    
    # After the colon there should be parameters
    parameters_match = re.search(r':(.+?)~', comment)
    if not parameters_match:
        log_error("No parameters found after the colon")
        return False
    parameters_str = parameters_match.group(1).strip()
    
    # Validate parameters based on the script tag
    script_tag = match.group(1)
    if script_tag in ['MASK', 'MA']:
        # Parameter for MASK Tag
        # Should have a minimum of 4 parameters, each separated by a comma
        parameters = [param.strip() for param in parameters_str.split(',') if param.strip()]
        if len(parameters) < 4 or not (parameters[0].isdigit() and parameters[1].isdigit()):
            log_error("Invalid parameters for MASK tag")
            return False
    elif script_tag in ['REPLACE', 'RE']:
        # Parameter for REPLACE Tag
        # Should have a minimum of 2 parameters, each separated by a comma
        # After every 2 parameters, there must be a semi colon (;)
        parameters = [param.strip() for param in re.split(r',|;', parameters_str) if param.strip()]
        if len(parameters) % 2 != 0 or len(parameters) < 2:
            log_error("Invalid parameters for REPLACE tag")
            return False
    elif script_tag in ['DROP', 'DR']:
        # Parameter for DROP Tag
        # Must only have 1 parameter
        parameters = [param.strip() for param in parameters_str.split(',') if param.strip()]
        if len(parameters) != 1:
            log_error("Invalid number of parameters for DROP tag")
            return False
    elif script_tag in ['RANDOM', 'RA']:
        # Parameter for RANDOM Tag
        # Example format: ~RA:+NNN(NNN) NNN-NNNN~
        # N - Numeric, A - Capital alpha characters, a - Lowercase alpha characters
        format_pattern = re.compile(r'([NAa])')
        valid_types = {'N', 'A', 'a'}
        parameters = format_pattern.findall(parameters_str)
        if set(parameters) <= valid_types:
            log_info("Valid parameters for RANDOM tag")
            return True
        else:
            log_error("Invalid parameters for RANDOM tag")
            return False
    elif script_tag in ['LIST', 'LI']:
        # Parameter for LIST Tag
        # Should have a maximum of 3 parameters
        # The first parameter must end with .txt
        # The second parameter must be a number
        # The third parameter must be either SEQ or RND
        parameters = [param.strip() for param in parameters_str.split(',') if param.strip()]
        if len(parameters) != 3:
            log_error("Invalid number of parameters for LIST tag")
            return False
        if not parameters[0].endswith('.txt') or not parameters[1].isdigit() or parameters[2] not in ['SEQ', 'RND']:
            log_error("Invalid parameters for LIST tag")
            return False

    # All requirements satisfied
    log_info("Valid comment")
    return True

if __name__ == "__main__":

    # Example Usage:
    comments = [
        "~MA:3,2,#,'@','.'~",
        "~MA:invalid,2,#,'@','.'~",  # Invalid first parameter for MASK
        "~RE:address,addr;'zone','co.uk'~",
        "~DROP:value1~",  # Valid DROP with 1 parameter
        "~DROP:value1,value2,value3~",  # Invalid number of parameters for DROP
        "~RA:+NNN(NNN) NNN-NNNN~",  # Valid RANDOM format
        "~LI:file.txt,10,SEQ~",  # Valid LIST with 3 parameters
        "~LI:file.txt,invalid,RND~",  # Invalid second parameter for LIST
    ]

    for comment in comments:
        result = validate_comment(comment)
        print(f"Comment: {comment}\nValid: {result}\n")