import re

def has_valid_brackets_format(s):
    if s.endswith('.'):
        return False
    
    if not (s.startswith('[') and s.endswith(']')):
        return False
    
    content = s[1:-1].strip()
    phrases = [phrase.strip() for phrase in content.split(',')]
    for phrase in phrases:
        if len(phrase.split()) > 3:
            return False
    return True

