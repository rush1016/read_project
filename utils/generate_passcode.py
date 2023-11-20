import random
import string

def generate_passcode(length=6):
    """Generate a random alphanumeric passcode."""
    characters = string.digits
    passcode = ''.join(random.choice(characters) for _ in range(length))
    return passcode