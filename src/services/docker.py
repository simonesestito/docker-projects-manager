import os
import yaml
from typing import List
from utils.shell import run_interactive_command

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

def get_compose_bind_mounts(dir: str):
    with open(os.path.join(dir, 'docker-compose.yml')) as compose_file:
        compose_yml = yaml.safe_load(compose_file)
        return [
            # Extract relative path from bind mount
            volume.split(':', maxsplit=1)[0]
            for service in compose_yml['services'].values()
            for volume in service.get('volumes', [])
            # Do not include volumes or absolute paths
            if volume.startswith('./')
        ]
