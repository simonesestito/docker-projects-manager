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
import shutil

from utils.print import print_ok


def create_file(file: str):
    if not os.path.isfile(file):
        with open(file, 'w'):
            pass # Create empty file

def copy_path(rel_path: str, src: str, dest: str):
    src_path = os.path.join(src, rel_path)
    dest_path = os.path.join(dest, rel_path)

    if os.path.isfile(src_path):
        # Create folder structure
        dirs = os.path.dirname(rel_path)
        os.makedirs(os.path.join(dest, dirs), exist_ok=True)

        # Copy the actual file
        shutil.copyfile(src_path, dest_path)

    elif os.path.isdir(src_path):
        # Create destination folder
        os.makedirs(dest_path, exist_ok=True)

        # Copy child files
        for file in os.listdir(src_path):
            copy_path(file, src_path, dest_path)

    print_ok(rel_path)