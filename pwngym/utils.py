import re

def print_colored(text, color="magenta"):
    # Define a dictionary of ANSI color codes
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }

    # Get the color code from the dictionary, or default to reset
    color_code = colors.get(color.lower(), colors['reset'])

    # Print the text in the specified color
    print(f"{color_code}{text}{colors['reset']}")

def winpath_escaper(path):
    # Escape backslashes in the path
    path = path.replace("\\", "\\\\")

    path = re.sub(r'\\\\\\+', r'\\\\', path)
    
    # First regex pattern to capture the part within parentheses
    first_regex = re.compile(r'(\\(.*)\ ([^\\]*)\\)')
    # Second regex pattern to find within the captured part
    second_regex = re.compile(r'(\ )')
    # Replacement text for the second regex
    replacement_text = r'\ '
    
    # Find all matches for the first regex
    matches = list(first_regex.finditer(path))
    
    # Initialize an offset to adjust replacement positions
    offset = 0
    
    # Loop through each match
    for match in matches:
        captured_text = match.group(1)  # Get the captured part        
        # Apply the second regex to replace within the captured part
        modified_text = second_regex.sub(replacement_text, captured_text)
        # Calculate the start and end positions adjusted by the current offset
        start = match.start(1) + offset
        end = match.end(1) + offset
        # Replace the original captured portion with the modified text
        path = path[:start] + modified_text + path[end:]
        
        # Update the offset by the difference in lengths between modified and original texts
        offset += len(modified_text) - len(captured_text)
    
    return re.sub(r'\\+ ', r'\ ', path)

def clean_byte_string(byte_str):
    # Define the regex for ANSI escape codes
    ansi_escape = re.compile(rb'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    # Remove ANSI escape codes
    byte_str = ansi_escape.sub(b'', byte_str)
    
    # Remove non-printable characters
    byte_str = bytes([b for b in byte_str if 32 <= b <= 126 or b in b'\t\n\r'])
    
    return byte_str

def check_keywords(keywords, command) -> bool:
        for word in keywords:
            if word in command:
                return True