from typing import List
from utils import run_interactive_command

def _compose_cmd(workdir: str, *args: List[str]):
    run_interactive_command('docker', 'compose', '--project-directory', workdir, *args)

def compose_up(dir: str):
    _compose_cmd(dir, 'up', '-d')

def compose_down(dir: str, delete_volumes: bool = False):
    if delete_volumes:
        _compose_cmd(dir, 'down', '--volumes')
    else:
        _compose_cmd(dir, 'down')

def compose_pull(dir: str):
    _compose_cmd(dir, 'pull')

def prune(all: bool = False):
    run_interactive_command('docker', 'system' if all else 'image', 'prune', '-a', '-f')