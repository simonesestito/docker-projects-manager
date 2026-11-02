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

import os
import sys
import yaml
from typing import List
from utils.print import print_err, print_warn
from utils.shell import run_interactive_command, run_quiet_command

def _compose_cmd(workdir: str, *args: List[str], exit_on_error: bool = True) -> int:
    return run_interactive_command(
        'docker', 'compose', '--project-directory', workdir, *args,
        exit_on_error=exit_on_error,
    )

def compose_up(dir: str):
    _compose_cmd(dir, 'up', '-d')

def compose_down(dir: str, delete_volumes: bool = False):
    if delete_volumes:
        _compose_cmd(dir, 'down', '--volumes')
    else:
        _compose_cmd(dir, 'down')

def compose_pull(dir: str):
    exit_code = _compose_cmd(dir, 'pull', exit_on_error=False)
    if exit_code == 0:
        return

    images = _compose_images(dir)
    missing_images = [image for image in images if not _image_exists(image)]
    if images and not missing_images:
        print_warn('Could not pull images, but all required images exist locally. Continuing.')
        return

    if missing_images:
        print_err(f'Images not available locally: {", ".join(missing_images)}')
    else:
        print_err('Could not determine the required Compose images')
    sys.exit(exit_code)


def _compose_images(dir: str) -> List[str]:
    result = run_quiet_command('docker', 'compose', '--project-directory', dir, 'config', '--images')
    if result.returncode != 0:
        return []
    return list(dict.fromkeys(
        line.strip() for line in result.stdout.splitlines() if line.strip()
    ))


def _image_exists(image: str) -> bool:
    return run_quiet_command('docker', 'image', 'inspect', image).returncode == 0

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
