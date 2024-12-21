import random
import string

ROLES = [
    ('member', 'Member'),
    ('worker', 'Worker'),
    ('admin', 'Admin')
]

def RandomString(n):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))