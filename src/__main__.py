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