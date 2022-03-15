def print_status(message: str):
    print(f'\n\033[96;1m{message}\033[0m')

def print_ok(message: str):
    print('\033[92;1m✓\033[0m ' + message)

def print_err(message: str):
    print('\033[91;1m✕\033[0m ' + message)