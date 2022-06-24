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

from services import git, docker
import sys, os
import shutil
from data import repo
from tempfile import TemporaryDirectory
from config import DOCKER_HOST_PROXY_PORT_VAR_NAME, PROJECT_FILES_TO_COPY
from processing.env import process_env_vars
from data.model import Project
from tasks.test import test_project
from utils.print import print_err, print_ok, print_status
import utils.io

def update_project(project: Project):
    print_status(f'Updating project {project.name}')

    # Clone repository
    with TemporaryDirectory() as repo_dir:
        print_status('Cloning project from git')
        git.clone_repo_temp(project.git_url, repo_dir)

        # Check if needs update
        git_commit = git.get_last_commit(repo_dir)
        if git_commit == project.last_commit:
            if len(sys.argv) >= 4 and sys.argv[3] == '-f':
                print_ok('Forcibly updating project')
            else:
                print_err(f'No update needed. Run "{sys.argv[0]} update {project.name} -f" to force an update.')
                return
        else:
            print_ok(f'Updating to commit {git_commit}')
            project.last_commit = git_commit
        
        # Copy necessary files
        print_status('Copying new files from cloned repository')
        for file in PROJECT_FILES_TO_COPY:
            utils.io.copy_path(file, repo_dir, project.dir_path)
        
        print_status('Copying required Docker bind mounts')
        for bind_path in docker.get_compose_bind_mounts(repo_dir):
            utils.io.copy_path(bind_path, repo_dir, project.dir_path)
        
        # Process environment variables
        print_status('Processing environment variables')
        cloned_env_file = os.path.join(repo_dir, '.env')

        # Process env file
        if os.path.isfile(project.env_file):
            shutil.copy(project.env_file, project.env_file + '.bak')
        else:
            print_err('.env file not found locally. Populate it with production env vars')

        process_env_vars(project.env_file, cloned_env_file, {
            DOCKER_HOST_PROXY_PORT_VAR_NAME: project.port,
        })

    # Update Docker
    print_status('Stopping old containers')
    docker.compose_down(project.dir_path)
    print_status('Pulling new images')
    docker.compose_pull(project.dir_path)
    print_status('Running new containers')
    docker.compose_up(project.dir_path)
    print_status('Removing unnecessary images')
    docker.prune()

    # Save project
    print_status('Saving project')
    repo.save_project(project)

    test_project(project)
