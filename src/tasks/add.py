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

import sys, os
from tempfile import NamedTemporaryFile
from config import WORK_DIR, SSH_KEY_FILE
from data import repo
from utils.print import print_status, print_err, print_ok
from utils.shell import run_interactive_command
from services.nginx import restart_nginx


def add_project():
    print_status('Creating new project')

    # Input data
    git_url = sys.argv[2] if len(sys.argv) > 2 else input('Git URL: ')
    project_name = sys.argv[3] if len(sys.argv) > 3 else input('Project name (and subdomain): ')
    if git_url.startswith('git@') and not os.path.isfile(SSH_KEY_FILE):
      print_err('No SSH key found in ' + SSH_KEY_FILE)

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

    # Save project
    print_status('Saving project')
    repo.save_project(project)

    print_ok(f'Populate .env file in {project.dir_path}, then run "{sys.argv[0]} update {project.name}"')