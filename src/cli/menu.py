from simple_term_menu import TerminalMenu

def show_menu(options: list, default=None) -> str:
    # options[i] = (key, display_value, return_value)
    if default is None:
        selected_index = TerminalMenu([v for _, v, _ in options]).show()
        selected_option = options[selected_index]
    else:
        selected_option = next(
            (option for option in options if option[0] == default),
            None
        )
        if selected_option is None:
            raise Exception("Invalid option: " + default)
    
    return selected_option[2]

def ask_yes_no(question: str, default: bool) -> bool:
    if default:
        reply = input(f'{question} [Y/n] ')
    else:
        reply = input(f'{question} [y/N] ')
    reply = reply.lower()

    if reply.startswith('y'): return True
    if reply.startswith('n'): return False
    return default