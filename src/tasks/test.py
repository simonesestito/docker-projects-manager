import requests
from config import DOCKER_HOST_PROXY_PORT_VAR_NAME
from data.model import Project
from utils.network import is_port_open
from utils.print import print_err, print_ok, print_status


def test_project(project: Project):
    print_status(f'Running tests on {project.name}')

    if is_port_open(project.port):
        print_ok(f'Port {project.port} is listening')
    else:
        print_err(f'Be sure to listen on {project.port} (env var = {DOCKER_HOST_PROXY_PORT_VAR_NAME})')
    
    try:
        http_response = requests.get(f'https://{project.domain_name}/')
        if http_response.status_code == 502:
            print_err('HTTP 502 Bad Gateway trying to connect via domain name. Make sure it didn\'t crash.')
        else:
            print_ok(f'HTTP request with result {http_response.status_code}')
    except Exception as e:
        print_err(e)
        print_err('Unable to connect to domain, double check DNS settings for ' + project.domain_name)
