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


def test_project(project: Project):
    print_status(f'Running tests on {project.name}')
    NUM_TRIES, TRY_SLEEP = 5, 0.5

    # Test port listening
    for _ in range(NUM_TRIES):
        time.sleep(TRY_SLEEP)
        if is_port_open(project.port):
            print_ok(f'Port {project.port} is listening')
            break
    else:
        print_err(f'Be sure to listen on {project.port} (env var = {DOCKER_HOST_PROXY_PORT_VAR_NAME})')
    
    # Test HTTP connection
    try:
        for _ in range(NUM_TRIES):
            time.sleep(TRY_SLEEP)
            http_response = requests.get(f'http://localhost:{project.port}')
            if http_response.status_code != 502:
                print_ok(f'HTTP request with result {http_response.status_code}')
                break
        else:
            print_err('HTTP 502 Bad Gateway trying to connect via localhost. Make sure it didn\'t crash.')
    except Exception as e:
        print_err(e)
        print_err('Unable to connect to domain, double check DNS settings for ' + project.domain_name)
