import os
import socket
from contextlib import closing
import subprocess
import sys
from typing import List

def run_interactive_command(*args: List[str]):
    print('> ' + ' '.join(args))
    exit_code = subprocess.Popen(
        args,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    ).wait()

    if exit_code:
        raise Exception(f'Interactive process terminated with exit code {exit_code}')

def create_file(file: str):
    if not os.path.isfile(file):
        with open(file, 'w'):
            pass # Create empty file

def print_status(message: str):
    print(f'\n\033[96;1m{message}\033[0m')

def print_ok(message: str):
    print('\033[92;1m✓\033[0m ' + message)

def print_err(message: str):
    print('\033[91;1m✕\033[0m ' + message)

def is_port_open(port: int, host: str = 'localhost'):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0
