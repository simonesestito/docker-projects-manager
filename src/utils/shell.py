'''
Copyright 2022 Simone Sestito
This file is part of "Docker Projects Manager".

"Docker Projects Manager" is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"Docker Projects Manager" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with "Docker Projects Manager".  If not, see <http://www.gnu.org/licenses/>.
'''

import subprocess
import sys
from typing import List

from utils.print import print_err


def run_interactive_command(*args: List[str], exit_on_error: bool = True) -> int:
    print('> ' + ' '.join(args))
    exit_code = subprocess.Popen(
        args,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    ).wait()

    if exit_code and exit_on_error:
        print_err(f'Interactive process terminated with exit code {exit_code}')
        sys.exit(exit_code)

    return exit_code


def run_quiet_command(*args: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
