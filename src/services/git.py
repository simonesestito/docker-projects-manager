from config import SSH_KEY_FILE
from cli import menu
import os
from services import ssh_key
from utils import run_interactive_command

def ask_for_ssh_key(git_url: str):
    if git_url.startswith('git@') and not os.path.isfile(SSH_KEY_FILE):
        if menu.ask_yes_no('Add SSH key?', True):
            ssh_key.save_ssh_key(ssh_key.input_ssh_key())

def clone_repo_temp(git_url: str, dest_dir: str):
    run_interactive_command('git', 'clone', git_url, dest_dir, '--depth=1')

def get_last_commit(repo_dir: str):
    with open(os.path.join(repo_dir, '.git', 'HEAD'), 'r') as git_head:
        head_file = git_head.read().split()[1]
    with open(os.path.join(repo_dir, '.git', head_file)) as git_head:
        return git_head.read().strip()