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


DEFAULT_TOP_DOMAIN_NAME = 'simonesestito.com'
HOME = os.getenv('HOME')
SSH_KEY_FILE = f'{HOME}/.ssh/id_rsa'
WORK_DIR = HOME
METADATA_JSON_FILE = 'docker-project-specs.json'
DEFAULT_MIN_PORT = 10_000
NGINX_CONFS_DIR = '/etc/nginx/sites-available'
NGINX_ENABLED_DIR = '/etc/nginx/sites-enabled'
PROJECT_FILES_TO_COPY = [ 'Dockerfile', 'docker-compose.yml', '.dockerignore' ]
DOCKER_HOST_PROXY_PORT_VAR_NAME = 'DOCKER_HOST_PROXY_PORT'
