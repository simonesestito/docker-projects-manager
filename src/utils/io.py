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
        os.makedirs(os.path.join(dest, dirs))

        # Copy the actual file
        shutil.copyfile(src_path, dest_path)

    elif os.path.isdir(src_path):
        # Create destination folder
        os.makedirs(dest_path)

        # Copy child files
        for file in os.listdir(src_path):
            copy_path(file, src_path, dest_path)

    print_ok(rel_path)