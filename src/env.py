import os
from typing import IO, List
from collections import OrderedDict
from utils import create_file, print_ok


def process_env_vars(local_env_file: str, cloned_env_file: str, override_vars: dict = None) -> List[str]:
    create_file(local_env_file)
    create_file(cloned_env_file)

    new_vars = OrderedDict()
    with open(local_env_file) as project_env, open(cloned_env_file) as cloned_env:
        old_vars = _parse_vars(project_env)
        curr_vars = _parse_vars(cloned_env)

    for key, curr_value in curr_vars.items():
        old_value = old_vars.get(key, '')
        if curr_value == old_value:
            print_ok(f'{key}="{old_value}"')
            new_value = old_value
        else:
            new_value = input(f'{key} [{curr_value}]:').strip()
            new_value = new_value or curr_value
        new_vars[key] = new_value

    # Override vars
    for key, value in override_vars.items():
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