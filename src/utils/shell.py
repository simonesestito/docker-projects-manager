import subprocess
import sys
from typing import List

from utils.print import print_err


def run_interactive_command(*args: List[str]):
    print('> ' + ' '.join(args))
    exit_code = subprocess.Popen(
        args,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    ).wait()

    if exit_code:
        print_err(f'Interactive process terminated with exit code {exit_code}')
        sys.exit(exit_code)