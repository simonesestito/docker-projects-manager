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
import sys
from cli import menu
from data import repo
from data.model import Project
from tasks import add, delete, test, update
from utils.print import print_err

def main():
    if os.getuid() == 0:
        raise Exception('Do not run this script as root.')

    selected_option = menu.show_menu([
        ('add', 'Add project', add.add_project),
        ('update', 'Update project', update.update_project),
        ('test', 'Test project', test.test_project),
        ('delete', 'Delete project', delete.delete_project),
    ], sys.argv[1] if len(sys.argv) > 1 else None)

    if selected_option.__code__.co_argcount == 0:
        selected_option()
    else:
        # It requires a project
        project = pick_project()
        if project is not None:
            selected_option(project)


def pick_project() -> Project:
    projects = repo.load_projects()
    if not projects:
        print_err('No projects found')
        return None

    return menu.show_menu([
        (project.name, project.name, project)
        for project in projects
    ], sys.argv[2] if len(sys.argv) > 2 else None)

if __name__ == '__main__':
    main()