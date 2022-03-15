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
import json
from typing import List

import validators
from config import DEFAULT_MIN_PORT, WORK_DIR, METADATA_JSON_FILE
from data.model import Project

def load_projects() -> List[Project]:
    return list(filter(lambda x: x is not None, (
        load_project(dir)
        for dir in os.listdir(WORK_DIR)
    )))

def save_project(project: Project):
    with open(project.spec_file_path, 'w') as spec_file:
        json.dump({
            'git_url': project.git_url,
            'port': project.port,
            'last_commit': project.last_commit,
        }, spec_file)

def add_project(name: str, git_url: str) -> Project:
    # Get next port number
    next_port = max((project.port for project in load_projects()), default=DEFAULT_MIN_PORT) + 1
    project = Project(
        name=name,
        git_url=git_url,
        port=next_port,
        last_commit='',
    )

    # Validate domain name
    validators.domain(project.domain_name)

    # Save project file
    os.mkdir(project.dir_path)
    with open(project.spec_file_path, 'w') as spec_file:
        json.dump({
            'git_url': project.git_url,
            'port': project.port,
            'last_commit': project.last_commit,
        }, spec_file)

    return project


def load_project(name: str) -> Project:
    try:
        with open(os.path.join(WORK_DIR, name, METADATA_JSON_FILE)) as specs_file:
            specs = json.load(specs_file)
            return Project(
                name=name,
                git_url=specs['git_url'],
                port=specs['port'],
                last_commit=specs['last_commit'],
            )
    except:
        return None
