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

import requests, time
from config import DOCKER_HOST_PROXY_PORT_VAR_NAME
from data.model import Project
from utils.network import is_port_open
from utils.print import print_err, print_ok, print_status

NUM_TRIES, TRY_SLEEP = 5, 0.5

def test_project(project: Project):
    print_status(f'Running tests on {project.name}')

    # Test port listening
    for _ in range(NUM_TRIES):
        time.sleep(TRY_SLEEP)
        if is_port_open(project.port):
            print_ok(f'Port {project.port} is listening')
            break
    else:
        print_err(f'Be sure to listen on {project.port} (env var = {DOCKER_HOST_PROXY_PORT_VAR_NAME})')
    
    # Test HTTP connection (localhost)
    _test_http(f'http://localhost:{project.port}')

    # Test HTTP connection (server)
    _test_http(f'https://{project.domain_name}')



def _test_http(url: str):
    host = url.split('://')[1].split(':')[0]
    last_err, last_status = None, None

    for _ in range(NUM_TRIES):
        time.sleep(TRY_SLEEP)
        last_err, last_status = None, None

        try:
            http_response = requests.get(url)
            last_status = http_response.status_code
            if last_status < 500:
                print_ok(f'HTTP request with result {http_response.status_code}, trying to connect via {host}.')
                return
        except Exception as e:
            last_err = e
    
    # Handle errors
    if last_status is not None:
        print_err(f'HTTP request failed with status {last_status}, trying to connect via {host}.')
    else: # last_err is not None
        print_err(f'HTTP request failed with error {last_err}, trying to connect via {host}.')