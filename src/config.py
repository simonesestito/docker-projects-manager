import os


DEFAULT_TOP_DOMAIN_NAME = 'simonesestito.com'
HOME = os.getenv('HOME')
SSH_KEY_FILE = f'{HOME}/.ssh/id_rsa'
WORK_DIR = HOME
METADATA_JSON_FILE = 'docker-project-specs.json'
DEFAULT_MIN_PORT = 10_000
NGINX_CONFS_DIR = '/etc/nginx/sites-available'
NGINX_ENABLED_DIR = '/etc/nginx/sites-enabled'
PROJECT_FILES_TO_COPY = [ 'docker-compose.yml' ]
DOCKER_HOST_PROXY_PORT_VAR_NAME = 'DOCKER_HOST_PROXY_PORT'