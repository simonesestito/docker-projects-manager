import sys
from tempfile import NamedTemporaryFile
from config import WORK_DIR
from services import git
from data import repo
from tasks.update import update_project
from utils.print import print_status
from utils.shell import run_interactive_command
from services.nginx import restart_nginx


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