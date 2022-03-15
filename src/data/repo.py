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
