from services import git, docker
import os
import shutil
from data import repo
from tempfile import TemporaryDirectory
from config import DOCKER_HOST_PROXY_PORT_VAR_NAME, PROJECT_FILES_TO_COPY
from processing.env import process_env_vars
from data.model import Project
from tasks.test import test_project
from utils import print_err, print_ok, print_status


def update_project(project: Project):
    print_status(f'Updating project {project.name}')

    # Clone repository
    with TemporaryDirectory() as repo_dir:
        print_status('Cloning project from git')
        git.clone_repo_temp(project.git_url, repo_dir)

        # Check if needs update
        git_commit = git.get_last_commit(repo_dir)
        if git_commit == project.last_commit:
            print_err('No update needed.')
            return
        else:
            print_ok(f'Updating to commit {git_commit}')
            project.last_commit = git_commit
        
        # Copy necessary files
        print_status('Copying new necessary files')
        for file in PROJECT_FILES_TO_COPY:
            from_file = os.path.join(repo_dir, file)
            dest_file = os.path.join(project.dir_path, file)
            if os.path.isfile(from_file):
                print_ok(file)
                shutil.copy(from_file, dest_file)
            else:
                print_err(file)
        
        # Process environment variables
        print_status('Processing environment variables')
        cloned_env_file = os.path.join(repo_dir, '.env')

        # Backup old env file
        if os.path.isfile(project.env_file):
            shutil.copy(project.env_file, project.env_file + '.bak')

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
