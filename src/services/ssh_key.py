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
from typing import List
from config import SSH_KEY_FILE

def input_ssh_key() -> List[str]:
    print('Paste your private SSH key here, in order to login to GitHub')
    print('It must end with -----END...')
    print()
    
    key = []
    while not key or not key[-1].startswith('-----END'):
        key.append(input())
    return key

def save_ssh_key(key: List[str], file: str = SSH_KEY_FILE):
    with open(file, 'w') as keyfile:
        keyfile.writelines(key)
    os.chmod(file, 0o0400)
