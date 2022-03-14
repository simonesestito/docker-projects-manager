from cProfile import run
import os
import shutil
import sys
from tempfile import TemporaryDirectory, NamedTemporaryFile
from env import process_env_vars
import menu
from model import Project
from nginx import restart_nginx
import repo
import git
import docker
from utils import print_err, print_ok, print_status, run_interactive_command
from config import DOCKER_HOST_PROXY_PORT_VAR_NAME, PROJECT_FILES_TO_COPY, WORK_DIR

def add_project():
    print_status('Creating new project')

    # Input data
    git_url = sys.argv[2] if len(sys.argv) > 2 else input('Git URL: ')
    project_name = sys.argv[3] if len(sys.argv) > 3 else input('Project name (and subdomain): ')
    git.ask_for_ssh_key(git_url)

    print_status(f'Saving new project to {WORK_DIR}')
    project = repo.add_project(project_name, git_url)
    
    # Add Nginx configuration
    print_status('Creating Nginx configuration')
    with NamedTemporaryFile() as nginx_temp_conf:
        nginx_temp_conf.write(f'''
        server {{
          listen 80;
          server_name {project.domain_name};
          location / {{
            include /etc/nginx/proxy-config-snippet.conf;
            proxy_pass http://localhost:{project.port}/;
          }}
        }}
        '''.encode())
        nginx_temp_conf.flush()
        run_interactive_command('sudo', 'cp', nginx_temp_conf.name, project.nginx_file)
    run_interactive_command('sudo', 'ln', '-s', project.nginx_file, project.nginx_link)
    restart_nginx()

    update_project(project)

def update_project(project: Project = None):
    if project is None:
        project = pick_project()
    
    if project is None:
        return

    print_status(f'Updating project {project.name}')

    # Clone repository
    with TemporaryDirectory() as repo_dir:
        print_status('Cloning project from git')
        git.clone_repo_temp(project.git_url, repo_dir)

        # Check if needs update
        with open(os.path.join(repo_dir, '.git', 'HEAD'), 'r') as git_head:
            head_file = git_head.read().split()[1]
        with open(os.path.join(repo_dir, '.git', *head_file.split('/'))) as git_head:
            git_commit = git_head.read()
            if git_commit == project.last_commit:
                print_err('No update is needed.')
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
    repo.save_project(project)

def delete_project(project: Project = None):
    if project is None:
        project = pick_project()
    
    if project is None:
        return

    print_status(f'Deleting project {project.name}')
    if not menu.ask_yes_no('Are you sure to delete this project?', False):
        print_err('Deletion cancelled.')
        return

    delete_volumes = menu.ask_yes_no('Delete volumes?', False)

    # Docker    
    print_status('Stopping Docker Compose')
    docker.compose_down(project.dir_path, delete_volumes)
    print_status('Cleaning Docker')
    docker.prune(all=True)

    # Nginx
    print_status('Removing Nginx configuration')
    run_interactive_command('sudo', 'rm', project.nginx_file, project.nginx_link)
    restart_nginx()

    # Project folder
    print_status('Removing project folder')
    shutil.rmtree(project.dir_path)
    

def pick_project() -> Project:
    projects = repo.load_projects()
    if not projects:
        print_err('No projects found')
        return None

    return menu.show_menu([
        (project.name, project.name, project)
        for project in projects
    ], sys.argv[2] if len(sys.argv) > 2 else None)

def main():
    if os.getuid() == 0:
        raise Exception('Do not run this script as root.')

    menu.show_menu([
        ('add', 'Add project', add_project),
        ('update', 'Update project', update_project),
        ('delete', 'Delete project', delete_project),
    ], sys.argv[1] if len(sys.argv) > 1 else None)()

if __name__ == '__main__':
    main()