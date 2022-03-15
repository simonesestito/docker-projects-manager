from utils.shell import run_interactive_command


def restart_nginx():
    run_interactive_command('sudo', 'nginx', '-t')
    run_interactive_command('sudo', 'systemctl', 'restart', 'nginx')