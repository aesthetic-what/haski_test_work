import hashlib
import os

def generate_token():
    random_bytes = os.urandom(32)
    return hashlib.sha256(random_bytes).hexdigest()
