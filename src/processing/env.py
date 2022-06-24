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

from typing import IO, List
from collections import OrderedDict
from utils.io import create_file
from utils.print import print_ok


def process_env_vars(local_env_file: str, cloned_env_file: str, override_vars: dict = None) -> List[str]:
    create_file(local_env_file)
    create_file(cloned_env_file)

    new_vars = OrderedDict()
    with open(local_env_file) as project_env, open(cloned_env_file) as cloned_env:
        old_vars = _parse_vars(project_env)
        curr_vars = _parse_vars(cloned_env)

    # Iterate through env vars found in cloned repo (probably, debug values)
    for key, curr_value in curr_vars.items():
        old_value = old_vars.get(key, None)
        if old_value is None:
            # Ask unknown env variables value
            new_value = input(f'{key} [{curr_value}]:').strip()
            new_value = new_value or curr_value
        else:
            print_ok(f'{key}="{old_value}"')
            new_value = old_value
        new_vars[key] = new_value

    # Override vars
    for key, value in override_vars.items():
        new_vars[key] = value

    # Add local env vars not found in previous steps
    for key, value in old_vars.items():
        if key not in new_vars:
            new_vars[key] = value
    
    # Finally, write new env vars
    with open(local_env_file, 'w') as project_env:
        project_env.writelines([
            f'{key}="{value}"'
            for key, value in new_vars.items()
        ])

def _parse_vars(env: IO) -> OrderedDict:
    return OrderedDict(
        var for var in (
            _parse_var(line) for line in env
        ) if var is not None
    )

def _parse_var(line: str):
    line = line.strip()
    if line.startswith('#') or '=' not in line:
        return None # Empty line or comment

    split_idx = line.index('=')
    key = line[:split_idx].strip()
    value = line[split_idx+1:].strip()

    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    return key, value
