import os
from typing import List
from config import SSH_KEY_FILE

def input_ssh_key() -> List[str]:
    key = []
    while not key or not key[-1].startswith('-----END'):
        key.append(input())
    return key

def save_ssh_key(key: List[str], file: str = SSH_KEY_FILE):
    with open(file, 'w') as keyfile:
        keyfile.writelines(key)
    os.chmod(file, 0o0400)
