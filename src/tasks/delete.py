import shutil
from data.model import Project
from services.nginx import restart_nginx
from utils.print import print_err, print_status
from services import docker
from cli import menu
from utils.shell import run_interactive_command


def delete_project(project: Project):
    print_status(f'Deleting project {project.name}')
    if not menu.ask_yes_no('Are you sure to delete this project?', False):
        print_err('Deletion cancelled.')
        return

    delete_volumes = menu.ask_yes_no('Delete volumes?', False)

    # Nginx
    print_status('Removing Nginx configuration')
    run_interactive_command('sudo', 'rm', project.nginx_file, project.nginx_link)
    restart_nginx()

    # Docker    
    print_status('Stopping Docker Compose')
    docker.compose_down(project.dir_path, delete_volumes)
    print_status('Cleaning Docker')
    docker.prune(all=True)

    # Project folder
    print_status('Removing project folder')
    shutil.rmtree(project.dir_path)
    


